import abc
import math
from itertools import chain, repeat
from typing import Any, Callable, Iterable, Union

import pandas as pd
from scop import Alldiff, Linear, Model, Quadratic

inf = math.inf


def to_iter(it, ref=None):
    """反復子化"""
    if not isinstance(it, str) and isinstance(it, Iterable):
        return it
    elif ref is None:
        return repeat(it)
    return [i for i, _ in zip(repeat(it), ref)]


class MyExpr(metaclass=abc.ABCMeta):
    """式（抽象クラス）"""

    type: Any = None  # scop.Constraintの型
    coe: Callable = None  # type: ignore # 係数を返す関数
    data: Callable = None  # type: ignore # 項目のイテラブルを返す関数

    @abc.abstractmethod
    def __init__(self):
        pass

    def __iter__(self):
        return iter((c, *d) for c, d in zip(self.coe(), self.data()))

    def to_constr(self, rhs, direction):
        assert isinstance(rhs, int) or isinstance(rhs, float), "rhs must be number"
        return MyConstraint(self, rhs, direction)

    def __eq__(self, rhs):
        return self.to_constr(rhs, "=")

    def __ge__(self, rhs):
        return self.to_constr(rhs, ">=")

    def __le__(self, rhs):
        return self.to_constr(rhs, "<=")

    def __add__(self, other):
        return MyPExpr(self, other)

    def __sub__(self, other):
        assert isinstance(other, MyExpr), "illegal other"
        return MyPExpr(self, MyMExpr(-1, other))

    def __mul__(self, k):
        return MyMExpr(k, self)

    def __truediv__(self, k):
        return MyMExpr(1 / k, self)


class MyLinear(MyExpr):
    """1次式"""

    type: Any = Linear

    def __init__(self, coe, var, val):
        self._coe = to_iter(coe, var)
        self._data = list(zip(var, to_iter(val)))

    def coe(self):
        return self._coe

    def data(self):
        return self._data


class MyQuadratic(MyLinear):
    """2次式"""

    type: Any = Quadratic

    def __init__(self, coe, var1, val1, var2, val2):
        self._coe = to_iter(coe, var1)
        self._data = list(zip(var1, to_iter(val1), var2, to_iter(val2)))


class MyMExpr(MyExpr):
    """MyExprの定数倍"""

    def __init__(self, k, expr):
        assert isinstance(k, int) or isinstance(k, float), "k must be number"
        self.k = k
        self.expr = expr
        self.type = expr.type

    def coe(self):
        return (self.k * i for i in self.expr.coe())

    def data(self):
        return self.expr.data()


class MyPExpr(MyExpr):
    """MyExpr同士の結合"""

    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
        self.type = expr1.type
        assert self.type == expr2.type, "Different type"

    def coe(self):
        return chain(self.expr1.coe(), self.expr2.coe())

    def data(self):
        return chain(self.expr1.data(), self.expr2.data())


class MyConstraint:
    """制約式（ex. MyExpr <= rhs）"""

    def __init__(self, expr, rhs, direction):
        assert isinstance(expr, MyExpr), "illegal expr"
        assert direction in {"=", "<=", ">="}, "illegal direction"
        self.expr = expr
        self.rhs = rhs
        self.direction = direction

    def scop_constr(self, name, weight):
        """scop.Constraintに変換"""
        cn = self.expr.type(
            name=name, weight=weight, rhs=self.rhs, direction=self.direction
        )
        for x in self.expr:
            cn.addTerms(*([i] for i in x))
        return cn


class MyAlldiff(MyConstraint):
    """全て異なる制約条件"""

    def __init__(self, vars):
        self.vars = vars

    def scop_constr(self, name, weight):
        """scop.Constraintに変換"""
        cn = Alldiff(name=name, weight=weight)
        for v in self.vars:
            cn.addVariable(v)
        return cn


class MyModel(Model):
    """モデル"""

    def addvars(
        self,
        num: Union[int, pd.DataFrame],
        domain: Iterable,
        pre: str = "v_",
        start: int = 0,
        var: str = "Var",
    ):
        """変数作成"""
        n, df = num, None
        if isinstance(num, pd.DataFrame):
            n, df = len(num), num
        v = [self.addVariable(f"{pre}{i + start:03}", domain) for i in range(n)]
        if df is not None:
            df[var] = v  # 変数の列作成
        return v

    def addcons(self, constr: MyConstraint, name: str = "", weight: float = 1):
        """制約条件追加"""
        assert isinstance(constr, MyConstraint), "illegal constr"
        self.addConstraint(constr.scop_constr(name, weight))

    def addvals(
        self, dfs: Union[pd.DataFrame, list], var: str = "Var", val: str = "Val"
    ):
        """結果の列作成"""
        if isinstance(dfs, pd.DataFrame):
            dfs = [dfs]
        for df in dfs:
            df[val] = [v.value for v in df[var]]
