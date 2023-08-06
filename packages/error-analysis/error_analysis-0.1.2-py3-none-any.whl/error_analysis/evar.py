"""
Data type for error propagation and ErrorModes
"""
import sympy
import matplotlib.pyplot as plt
import weakref
import numpy as np
import warnings
from varname import varname
from error_analysis import options, tools


# TODO check for circular expression and either add warning or fix
# TODO add support for units
class evar:
    """
    Data type which supports error propagation.

    Since most parameters can fall back to options, all non-optional parameters are marked.
    """
    __var_dic = dict()
    __dic_id = 0
    __gc_prevention = []

    def __init__(self, value=None, gauss_error=None, max_error=None, name=None, unit=None):
        """
        Parameters
        ----------
        value: float or list, not optional
            The value/s of the variable. Can be list or single value
        gauss_error: float or list
            error which is propagated by gaussian estimation.
        max_error:  float or list
            error which is propagated by maximum error estimation.
        name: string
            Display name in everything string related. Can be latex style
        unit
            not implemented yet

        Notes
        ----------
        This data type can both function as a list or a single value. If this is an instance all operations will be
        perfomed element wise. So

            a*b = a_i*b_i.
        The error parameters are optional and can be floats or lists. A non-set error will be assumed to be zero.
        If the value of an instance is a list but only a single error is provided, it will be transformed to a list.

        Examples
        ----------

            evar([1,2], max_err= 0.5) = (1 +- 0 +- 0.5), (2 +- 0 +- 0.5)
            evar(4,2) = (4 +- 2 +- 0)
        """

        # keep track of all involved variables
        # it should be tested if this is really faster than iterating over all existing variables
        self.value = None
        """Where actual value/s are stored. Is either np.ndarray or single value"""
        self.gauss_error = None
        """Where actual gauss errors are stored. Is either np.ndarray or single value"""
        self.max_error = None
        """Where actual max errors are stored. Is either np.ndarray or single value"""
        if unit is not None:
            # add unit support for operands.
            print("thats not finished yet")

        if name == "INT_OP":
            self.name = "unknown"
            self.__id = -1
            self.has_gauss_error = True
            self.has_max_error = True
        else:
            self.__dependencies = set()
            self.__id = evar.__dic_id
            self.__dependencies.add(self.__id)
            if not options.correct_garbage_collection:
                evar.__gc_prevention.append(self)
            evar.__dic_id += 1
            # to ensure correct garbage collection
            evar.__var_dic[self.__id] = weakref.ref(self)

            self.symbol = sympy.symbols("v" + str(self.__id) + "v", real=True)
            self.g_symbol = sympy.symbols("g" + str(self.__id) + "g", real=True)
            self.m_symbol = sympy.symbols("m" + str(self.__id) + "m", real=True)
            self.__expr = self.symbol
            self.__shadow_expr = self.__expr
            self.__shadow_dependencies = self.__dependencies
            self.has_gauss_error = True
            self.has_max_error = True
            # value of var init
            if value is None:
                self.is_list = False
                self.value = 0
                self.length = 1
            else:
                if (type(value) is list) or (type(value) is np.ndarray):
                    self.is_list = True
                    self.length = len(value)
                    self.value = np.array(value)

                else:
                    self.is_list = False
                    self.length = 1
                    self.value = value
            # gaussian error init
            if gauss_error is None:
                self.has_gauss_error = False
                if self.length == 1:
                    self.gauss_error = 0
                else:
                    self.gauss_error = np.zeros(self.length)
            else:
                if type(gauss_error) == list:
                    if len(gauss_error) != self.length:
                        raise Exception("Size of value and gauss error don't match")
                    self.gauss_error = np.array(gauss_error)
                else:
                    if self.length == 1:
                        self.gauss_error = gauss_error
                    else:
                        self.gauss_error = np.full(self.length, gauss_error)

            # maximum error init
            if max_error is None:
                self.has_max_error = False
                if self.length == 1:
                    self.max_error = 0
                else:
                    self.max_error = np.zeros(self.length)
            else:
                if type(max_error) == list:
                    if len(max_error) != self.length:
                        raise Exception("Size of value and max error don't match")
                    self.max_error = max_error
                else:
                    if self.length == 1:
                        self.max_error = max_error
                    else:
                        self.max_error = np.full(self.length, max_error)

            # set name
            if name is None:
                self.name = str(varname(raise_exc=False))
                # format accordingly e.g. E_g to E_{g}
            else:
                self.name = name

    def get_expr(self, as_latex=None, with_name=True):
        """
        Gets expression (equation) of this variable

        Parameters
        ----------
        as_latex : bool
            wether to make this latex ready or more readable for console. Default is defined by options
        with_name : bool
            wether to add name in front

        Returns
        -------
        expression as string
        """
        as_latex = options.as_latex if as_latex is None else as_latex
        expr, dependencies = self.__get_expr()
        if options.simplify_eqs:
            expr = sympy.simplify(expr)
        expr = self.__replace_ids(sympy.latex(expr)) if as_latex else self.__replace_ids(str(expr))
        if with_name:
            expr = self.name + " = " + expr
        return expr

    def get_error(self, error_mode=None, error_vars=None, as_latex=None, with_name=True):
        """
        Get equation of error/s

        Parameters
        ----------
        error_mode : ErrorMode
            Which error type you want to retrieve.
        error_vars : list of evars
            Errors will be calculated only in respect to these. Standard is every variable that has error
        as_latex : bool
            wether to print latex style
        with_name : bool
            wether to print error name in front
        Returns
        -------
            error equation/s as string
        """
        error_mode = options.error_mode if error_mode is None else error_mode
        if error_mode == ErrorMode.NONE:
            return ""
        if error_mode == ErrorMode.BOTH:
            return self.get_error(ErrorMode.GAUSS, error_vars, as_latex, with_name) + "\n" + \
                   self.get_error(ErrorMode.MAX, error_vars, as_latex, with_name)
        if error_mode == ErrorMode.COMBINED:
            temp = options.gauss_error_name
            options.gauss_error_name = ""
            ret = self.get_error(ErrorMode.GAUSS, error_vars, as_latex, with_name)
            options.gauss_error_name = temp
            return ret
        if as_latex is None:
            as_latex = options.as_latex
        expr, dependencies = self.__get_expr()
        if error_vars is None:
            error_vars = []
            for i in dependencies:
                entry = evar.__var_dic[i]()
                if entry.has_gauss_error and error_mode == 0:
                    error_vars.append(entry)
                if entry.has_max_error and error_mode == 1:
                    error_vars.append(entry)
        err = None
        if error_mode == 0:
            err = tools.get_gauss_expr(expr, error_vars)
        else:
            err = tools.get_max_expr(expr, error_vars)
        if options.simplify_eqs:
            err = sympy.simplify(err)
        err = self.__replace_ids(sympy.latex(err)) if as_latex else self.__replace_ids(
            str(err))
        if with_name:
            if error_mode == ErrorMode.MAX:
                err = r"\sigma_{" + options.max_error_name + "_{" + self.name + "}}" + " = " + err
            if error_mode == ErrorMode.GAUSS:
                err = r"\sigma_{" + options.gauss_error_name + "_{" + self.name + "}}" + " = " + err
        return err

    def get_gauss_error(self, error_vars=None, as_latex=None, with_name=True):
        """
        calls get_error with `ErrorMode.GAUSS`

        Parameters are equal to `get_error`.
        """
        return self.get_error(ErrorMode.GAUSS, error_vars, as_latex, with_name)

    def get_max_error(self, error_vars=None, as_latex=None, with_name=True):
        """
        calls get_error with `ErrorMode.MAX`

        Parameters are equal to `get_error`.
        """
        return self.get_error(ErrorMode.MAX, error_vars, as_latex, with_name)

    # TODO add support for options.error_mode
    # TODO use proper functions
    def show(self, font_size=12):
        """
        Shows screen with all equations and values

        Parameters
        -------
        font_size : int
            font size of everything
        """
        text = ""
        text += "$" + self.get_expr(as_latex=True) + "$\n"
        text += "$" + self.get_gauss_error(as_latex=True) + "$\n"
        text += "$" + self.get_max_error(as_latex=True) + "$\n"
        t_str = self.get_value_str(as_latex=True)
        t_str = t_str.replace("\n", "$\n$")
        text += "$" + t_str + "$"
        plt.text(0, 0.1, text, fontsize=font_size)
        plt.axis("off")
        plt.show()

    def get_combined_error(self):
        """
        Combines errors by assuming errors are independet.

            sig_combined = sqrt(sig_gauss**2+sig_max**2)

        Returns
        -------
        combined error
        """
        return np.sqrt(self.gauss_error ** 2 + self.max_error ** 2)

    def __str__(self):
        """
        Calls get_value_str with parameters specified in options

        Returns
        -------
        formatted string
        """
        return self.get_value_str()

    # TODO less lazy version that runs faster. especially if garbage_colleciton=false
    # TODO fix non scientific version
    # FIXME add trailing zeros. e.g. (5.1+-0.33)=(5.10+-0.33)
    def get_value_str(self, error_mode=None, as_latex=None, no_rounding=None, scientific=True):
        """
        Get value or values of this instance formatted

        Returns
        -------
        error_mode : ErrorMode
            See `ErrorMode`
        as_latex : bool
            See `error_analysis.options.as_latex`
        no_rounding : bool
            See `error_analysis.options.no_rounding`
        scientific : bool
            wether to format in scientific notation or not

        Returns
        -------
        formatted string
        """
        no_rounding = options.no_rounding if no_rounding is None else no_rounding
        as_latex = options.as_latex if as_latex is None else as_latex
        error_mode = options.error_mode if error_mode is None else error_mode
        pm = r" \pm " if as_latex else " +- "
        times = r"\cdot " if as_latex else "* "
        if self.length == 1:
            if not np.isfinite(self.value):
                warnings.warn("Value is not real number. Behaviour in equations undefined. Did you perform bad "
                              "operation like log(-5)?")
                return self.name + " = " + str(self.value) + " +- " + str(self.gauss_error) + " +- " + str(
                    self.max_error)
            a, b, c, d = 0, 0, 0, 0
            first_error = self.get_combined_error() if error_mode == ErrorMode.COMBINED else self.gauss_error
            if not np.isfinite(self.gauss_error) or not np.isfinite(self.max_error):
                warnings.warn("On of the errors is not real number. Behaviour in equations undefined. Did you perform"
                              " bad operation like log(-5)?")
                return self.name + " = " + str(self.value) + " +- " + str(self.gauss_error) + " +- " + str(
                    self.max_error)
            a, b, c, d = tools.transform_to_sig(self.value, first_error, self.max_error, no_rounding)
            if not scientific:
                a, b, c, d = tools.transform_to_sig(self.value, first_error, self.max_error, no_rounding)
                a *= 10 ** d
                b *= 10 ** d
                c *= 10 ** d
            dec_exp = ""
            if d == 0 or not scientific:
                pass
            elif d == 1:
                dec_exp = times + "10"
            else:
                dec_exp = times + "10^{" + str(d) + "}"

            error_str = ""
            if error_mode == ErrorMode.NONE:
                return self.name + " = " + str(a) + " " + dec_exp
            elif error_mode == ErrorMode.BOTH:
                error_str = pm + str(b) + pm + str(c)
            elif error_mode == ErrorMode.MAX:
                error_str = pm + str(c)
            elif error_mode == ErrorMode.GAUSS:
                error_str = pm + str(b)
            elif error_mode == ErrorMode.COMBINED:
                error_str = pm + str(b)
            return self.name + " = (" + str(a) + error_str + ") " + dec_exp

        else:
            string = ""
            for i in range(self.length):
                string += self[i].get_value_str(error_mode, as_latex, no_rounding, scientific) + "\n"
            return string[:-1]

    # TODO should return equations in align etc
    def to_str(self, print_values=False, print_expr=False, print_gauss_error=False, print_max_error=False,
               print_all=False, as_latex=options.as_latex):
        """
        .. warning:: Unfinished. Do not use!
        """
        ret_str = ""
        if print_values == False and print_expr == False and print_gauss_error == False and print_max_error == False and print_all == False:
            ret_str = self.name
        if print_all:
            print_values = True
            print_expr = True
            print_gauss_error = True
            print_max_error = True
        if print_values:
            ret_str += self.get_value_str(as_latex)
            if print_gauss_error or print_max_error or print_expr:
                ret_str += "\n"
        if print_expr:
            ret_str += self.name + "=" + self.get_expr(as_latex)
            if print_gauss_error or print_max_error:
                ret_str += "\n"
        if print_gauss_error:
            ret_str += r"\sigma_{" + options.gauss_error_name + "_{" + self.name + "}}" + "=" + self.get_gauss_error(
                as_latex=as_latex)
            if print_max_error:
                ret_str += "\n"
        if print_max_error:
            ret_str += r"\sigma_{" + options.max_error_name + "_{" + self.name + "}}" + "=" + self.get_max_error(
                as_latex=as_latex)
        return ret_str

    def __getitem__(self, key):
        """
        Return i'th variable or sliced variable.

        Parameters
        -------
        key : index, slice
            either single number or something like a:b:c

        Returns
        -------
        sliced variable if instance is list. otherwise returns value key=0, sig key=1, max key=2

        Examples
        -------
        just like you would use normal lists. All operations are supported e.g. a[1], a[1:4], a[3:6:2] a[-1].....
        """
        if self.length > 1:
            name = ""
            if type(key) is int:
                name = self.name + "_{" + str(key) + "}"
            else:
                name = self.name
            return evar(self.value[key], self.gauss_error[key], self.max_error[key], name)

        else:
            if key == 0:
                return self.value
            elif key == 1:
                return self.gauss_error
            elif key == 2:
                return self.max_error
            else:
                raise IndexError("list index out of range")

    # TODO add check for correlations. sig_stat(x-x+d) e.g. should  just be sig_stat(d)
    # operators
    def __finish_operation(self):
        if type(self.value) is np.ndarray:
            self.length = len(self.value)
            if np.count_nonzero(self.gauss_error) > 0:
                self.has_gauss_error = True
            else:
                self.has_gauss_error = False
            if np.count_nonzero(self.max_error) > 0:
                self.has_max_error = True
            else:
                self.has_max_error = False
        else:
            self.length = 1
            if self.gauss_error == 0:
                self.has_gauss_error = False
            else:
                self.has_gauss_error = True
            if self.max_error == 0:
                self.has_max_error = False
            else:
                self.has_max_error = True

    # TODO implement iadd isub imul itruediv completely
    # + and -
    # +
    def __add__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value + other.value
            RET_VAR.gauss_error = np.sqrt(self.gauss_error ** 2 + other.gauss_error ** 2)
            RET_VAR.max_error = np.abs(self.max_error) + np.abs(other.max_error)
            RET_VAR.__expr = self.__expr + other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value + other
            RET_VAR.gauss_error = self.gauss_error
            RET_VAR.max_error = self.max_error
            RET_VAR.__expr = self.__expr + other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        if type(other) == evar:
            raise NotImplementedError("Currently only supported with numbers or lists but not evar")
        else:
            self.value += other
            self.__expr += other
            return self

    # -
    def __sub__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value - other.value
            RET_VAR.gauss_error = np.sqrt(self.gauss_error ** 2 + other.gauss_error ** 2)
            RET_VAR.max_error = np.abs(self.max_error) + np.abs(other.max_error)
            RET_VAR.__expr = self.__expr - other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value - other
            RET_VAR.gauss_error = self.gauss_error
            RET_VAR.max_error = self.max_error
            RET_VAR.__expr = self.__expr - other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    # TODO make this less lazy and more efficient
    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        if type(other) == evar:
            raise NotImplementedError("Currently only supported with numbers or lists but not evar")
        else:
            self.value -= other
            self.__expr -= other
            return self

    def __neg__(self):
        RET_VAR = evar(name="INT_OP")
        RET_VAR.name = self.name
        RET_VAR.value = -self.value
        RET_VAR.gauss_error = self.gauss_error
        RET_VAR.max_error = self.max_error
        RET_VAR.__expr = -self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    # * and /
    # *
    def __mul__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value * other.value
            RET_VAR.gauss_error = np.sqrt((other.gauss_error * self.value) ** 2 + (other.value * self.gauss_error) ** 2)
            RET_VAR.max_error = np.abs(other.max_error * self.value) + np.abs(self.max_error * other.value)
            RET_VAR.__expr = self.__expr * other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value * other
            RET_VAR.gauss_error = self.gauss_error * other
            RET_VAR.max_error = self.max_error * other
            RET_VAR.__expr = self.__expr * other
            RET_VAR.__dependencies = self.__dependencies
            RET_VAR.name = self.name
        RET_VAR.__finish_operation()
        return RET_VAR

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        if type(other) == evar:
            raise NotImplementedError("Currently only supported with numbers or lists but not evar")
        else:
            self.max_error *= abs(other)
            self.gauss_error *= abs(other)
            self.value *= other
            return self

    # /

    def __truediv__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value / other.value
            RET_VAR.gauss_error = np.sqrt(
                (other.gauss_error * self.value) ** 2 + (other.value * self.gauss_error) ** 2) / (other.value ** 2)
            RET_VAR.max_error = np.abs(other.max_error * self.value / other.value ** 2) + np.abs(
                self.max_error / other.value)
            RET_VAR.__expr = self.__expr / other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value / other
            RET_VAR.gauss_error = self.gauss_error / other
            RET_VAR.max_error = np.abs(self.max_error / other)
            RET_VAR.__expr = self.__expr / other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __rtruediv__(self, other):
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = other / self.value
        RET_VAR.gauss_error = other * np.abs(self.gauss_error) / self.value ** 2
        RET_VAR.max_error = other * np.abs(self.max_error / self.value ** 2)
        RET_VAR.__expr = other / self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __itruediv__(self, other):
        if type(other) == evar:
            raise NotImplementedError("Currently only supported with numbers or lists but not evar")
        else:
            if other == 0:
                raise Exception("Divide by zero encountered. Math police is on their way")
            self.max_error = self.max_error / abs(other)
            self.gauss_error = self.gauss_error / abs(other)
            self.value = self.value / other
            return self

    # ^
    def __pow__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value ** other.value
            inner = (self.gauss_error * other.value) ** 2 + (other.gauss_error * self.value * np.log(self.value)) ** 2
            RET_VAR.gauss_error = np.sqrt(inner * self.value ** (2 * other.value - 2))
            RET_VAR.max_error = np.abs(self.max_error * other.value * self.value ** (other.value - 1)) + np.abs(
                other.max_error * np.log(self.value) * self.value ** other.value)
            RET_VAR.__expr = self.__expr ** other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value ** other
            RET_VAR.gauss_error = np.sqrt(self.value ** (2 * other - 2)) * np.abs(self.gauss_error * other)
            RET_VAR.max_error = np.abs(self.max_error * other * self.value ** (other - 1))
            RET_VAR.__expr = self.__expr ** other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __rpow__(self, other):
        # other**self
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = other ** self.value
        RET_VAR.gauss_error = np.abs(self.gauss_error) * np.log(other) * other ** self.value
        RET_VAR.max_error = np.abs(self.max_error) * np.log(other) * other ** self.value
        RET_VAR.__expr = other ** self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __ipow__(self, other):
        if type(other) == evar:
            raise NotImplementedError("Currently only supported with numbers or lists but not evar")
        else:
            self.value **= other
            self.gauss_error = np.abs(self.gauss_error) * np.log(other) * other ** self.value
            self.max_error = np.abs(self.max_error) * np.log(other) * other ** self.value
            return self

    def __del__(self):
        if self.__id != -1:
            del self.symbol
            del self.m_symbol
            del self.g_symbol
            del evar.__var_dic[self.__id]

    def set_name(self, name):
        """
        Sets name for this variable and also makes it a "real" variable.
        Using it in equations will now longer give expression of defining equation of this variable

        Parameters
        -------
        name : string
            the new name for the variable
        """
        if self.__id == -1:
            self.__shadow_expr = self.__expr
            self.__shadow_dependencies = self.__dependencies
            self.__id = evar.__dic_id
            self.__dependencies = {self.__id}
            evar.__dic_id += 1
            evar.__var_dic[self.__id] = weakref.ref(self)
            self.symbol = sympy.symbols("v" + str(self.__id) + "v")
            self.g_symbol = sympy.symbols("g" + str(self.__id) + "g")
            self.m_symbol = sympy.symbols("m" + str(self.__id) + "m")
            self.__expr = self.symbol
            self.name = name
            self.__finish_operation()
        else:
            self.name = name

    def to_variable(self, name):
        """
        Same as set_name. Exists for backwards compatability
        Parameters
        ----------
        name
            new name of this instance
        """
        self.set_name(name)

    def __get_expr(self):
        if self.__id == -1:
            if options.simplify_eqs:
                return sympy.simplify(self.__expr), self.__dependencies
            else:
                return self.__expr, self.__dependencies
        else:
            if options.simplify_eqs:
                return sympy.simplify(self.__shadow_expr), self.__shadow_dependencies
            else:
                return self.__shadow_expr, self.__shadow_dependencies

    def __replace_ids(self, string):
        temp_str = string
        expr, dependencies = self.__get_expr()
        for i in dependencies:
            num = i
            temp_str = temp_str.replace("v" + str(num) + "v", evar.__var_dic[num]().name)
            temp_str = temp_str.replace("g" + str(num) + "g",
                                        r"\sigma_{" + options.gauss_error_name + "_{" + evar.__var_dic[
                                            i]().name + "}}")
            temp_str = temp_str.replace("m" + str(num) + "m",
                                        r"\sigma_{" + options.max_error_name + "_{" + evar.__var_dic[i]().name + "}}")
        return temp_str

    def __len__(self):
        return self.length


class ErrorMode(enumerate):
    """
    All available modes for getting errors

    Examples
    Suppose we have

        a = (15 +-1 +-2)
    Than the different modes will look like

        GAUSS, a = (15 +-1)
        MAX, a = (15 +-2)
        BOTH = (15 +-1 +-2)
        COMBINED a = (15.0 +-2.2)
        NONE a = 15
    -------
    """
    GAUSS = 0
    """only gauss error. is usually statistical error"""
    MAX = 1
    """only max error. is usually systematic error"""
    BOTH = 2
    """ both at the same time """
    COMBINED = 3
    """ combined to one error with sigma= sqrt(gauss^2+max^2) """
    NONE = 4
    """ no errors"""
