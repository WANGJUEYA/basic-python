# 创建设备类
import time

from sympy import *


class Machine():  # 设备类
    def __init__(self, m, n, q, x, y, tstart, a, b):  # mn威布尔参数，q是Machine对应的产能，XY是维护决策，tstar是任务开始时间，a是pm能力
        t = symbols('t')  # 约定变量t
        failure = x * a * (m / n) * ((t - b * tstart) / n) ** (m - 1) + y * (m / n) * ((t - tstart) / n) ** (m - 1) + (
                1 - x - y) * (m / n) * (t / n) ** (m - 1)  # 故障率更新
        self.qup = 0
        self.qdown = q
        self.up = (1 - failure)
        self.down = failure


class Station():  # 工序类
    def __init__(self, failures, capacitys):
        self.product = capacitys
        self.failure = failures


# 并联获得的概率
def F_uni_par(machines):
    F_state = []
    for machine in machines:
        F_machine = ([machine.up, machine.down])
        F_state.append(F_machine)
    from itertools import product
    F_total = []
    for stationf in product(*F_state):
        F_total.append(np.prod(stationf))  # 对列表数据累乘
    return (F_total)


# 并联对应的产能损失

def P_uni_par(machines):
    P_state = []
    for machine in machines:
        P_machine = ([machine.qup, machine.qdown])
        P_state.append(P_machine)
    from itertools import product
    P_total = []
    for stationp in product(*P_state):
        P_total.append(sum(stationp))  # 对列表数据累加
    return (P_total)


def F_uni_ser(stations):
    t = symbols('t')  # 约定变量t
    F_line = []
    for station in stations:
        F_line.append(station.failure)
    from itertools import product
    F_all = []
    for fline in product(*F_line):
        f_all = np.prod(fline)
        F_all.append(f_all)
    return (F_all)


# 串联对应的产能损失
def P_uni_ser(stations):
    P_line = []
    for station in stations:
        P_line.append(station.product)
    from itertools import product
    P_all = []
    for pline in product(*P_line):
        P_all.append(max(*pline))
    return (P_all)


def Capacity(P, F, tstart, tend, Tc, Pline):
    import numpy as np
    t = symbols('t')  # 约定变量t
    from scipy.integrate import quad
    solution = []
    for ff in F:
        f_func = lambdify(t, ff)
        f_solution = quad(f_func, tstart, tend)
        solution.append(f_solution[0])
    F_result = np.multiply(np.array(P), np.array(solution))
    actual_capacity = (tend - tstart - sum(F_result) * Tc) * Pline
    return (actual_capacity)


# 能耗计算
def energy(machines, tstart, tend, Tc, p_normal, p_fix):
    Line_energy = []
    machine_energy = []
    t = symbols('t')  # 约定变量t
    for machine in machines:
        from scipy.integrate import quad
        fmodify = lambdify(t, machine.down)
        singletime = quad(fmodify, tstart, tend)
        stop_time = singletime[0] * Tc
        machine_energy = (tend - tstart - stop_time) * p_normal + stop_time * p_fix
        Line_energy.append(machine_energy)
    return (sum(Line_energy))


# 构造启发式获得初始解
def generate(capacity, tpm, tpr, T_limit):
    import random
    T_left = T_limit
    x = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    capacity_fix = capacity[:]
    capacity_pr = capacity[:]
    capacity_pm = capacity[:]
    while len(capacity_pm) > 0:
        if random.randint(0, 100) <= 70:  # 决定是否随机生成
            if len(capacity_pr) > 0:  # 是否从pr集合里面挑选
                place_pr = capacity_pr.index(max(capacity_pr))  # 找到最大值的位置
                del capacity_pr[place_pr]
                if T_left - tpr[place_pr] >= 0:
                    T_left = T_left - tpr[place_pr]  # 更新维护时间
                    y[place_pr] = 1
                    capacity_fix[place_pr] = 0
                    capacity_pm[place_pr] = 0
            else:  # 是否从pm集合里面挑选
                place_pm = capacity_pm.index(max(capacity_pm))
                if max(capacity_pm) == 0:
                    del capacity_pm[place_pm]
                    break
                if T_left - tpm[place_pm] > 0:
                    T_left = T_left - tpm[place_pm]  # 更新维护时间
                    x[place_pm] = 1
                    capacity_fix[place_pm] = 0
        else:
            if len(capacity_fix) > 0:
                place_rand = random.randint(0, len(capacity_fix) - 1)  # 随机选取
                if capacity_fix[place_rand] == 0:
                    del capacity_fix[place_rand]
                    continue
                elif T_left - tpr[place_rand] > 0:
                    T_left = T_left - tpr[place_rand]
                    y[place_rand] = 1
                    del capacity_fix[place_rand]
                elif T_left - tpm[place_rand] > 0:
                    T_left = T_left - tpm[place_rand]
                    x[place_rand] = 1
                    del capacity_fix[place_rand]
                else:
                    del capacity_fix[place_rand]
                    continue
            else:
                break
    return (x, y)


# 从第二个生产周期开始
import numpy as np

t = symbols('t')
m = [3, 1.6, 2.2, 1.8, 2.6, 3.2, 1.3, 2.5, 2.8]
n = [8000, 7200, 10000, 12000, 9600, 15000, 11000, 9400, 16600]
capacity = [0.7, 0.3, 0.2, 0.5, 0.3, 0.1, 0.5, 0.1, 0.3]
ability = [0.7, 0.3, 0.2, 0.5, 0.3, 0.1, 0.5, 0.1, 0.3]
tstart = 7000  # 任务开始时间
tend = 15000  # 任务结束时间
tpm = [16, 15, 23, 16, 18, 17, 19, 25, 20]  # pm时间
tpr = [90, 100, 87, 95, 78, 60, 88, 97, 88]  # pr时间
a = [1.02, 1.10, 1.04, 1.05, 1.1, 1.09, 1.12, 1.07, 1.03]  # 故障率加速因子
b = [0.9, 0.8, 0.85, 0.75, 0.69, 0.87, 0.86, 0.79, 0.83]  # 役龄递减因子
T_limit = 200  # 维护限制时间

# 计算100次
Embed_Energy = []
x_dic = []
y_dic = []
time_total = 50
for i in range(0, time_total):  # time_total次里面取最优

    (x, y) = generate(capacity, tpm, tpr, T_limit)
    T_pm = list(map(lambda x: x[0] * x[1], zip(tpm, x)))
    T_pr = list(map(lambda x: x[0] * x[1], zip(tpr, y)))
    if sum(T_pm + T_pr) > T_limit:
        print("There are something wrong")
    Machine_line = []
    # 写一个是否重复出现
    if x not in x_dic and y not in y_dic:
        x_dic.append(x)
        y_dic.append(y)
        Machine_line = []
        for j in range(0, 9):
            my_machine = Machine(m[j], n[j], ability[j], x[j], y[j], tstart, a[j], b[j])
            Machine_line.append(my_machine)
        machines_station1 = [Machine_line[0], Machine_line[1]]
        machines_station2 = [Machine_line[2], Machine_line[3], Machine_line[4]]
        machines_station3 = [Machine_line[5], Machine_line[6], Machine_line[7], Machine_line[8]]
        F_Station1 = F_uni_par(machines_station1)
        F_Station2 = F_uni_par(machines_station2)
        F_Station3 = F_uni_par(machines_station3)
        P_Station1 = P_uni_par(machines_station1)
        P_Station2 = P_uni_par(machines_station2)
        P_Station3 = P_uni_par(machines_station3)
        Station1 = Station(F_Station1, P_Station1)
        Station2 = Station(F_Station2, P_Station2)
        Station3 = Station(F_Station3, P_Station3)
        Stations = [Station1, Station2, Station3]
        P = P_uni_ser(Stations)
        F = F_uni_ser(Stations)
        Actual_Capacity = Capacity(P, F, tstart, tend, 20, 50)
        Actual_Energy = energy(Machine_line, tstart, tend, 20, 30, 80)
        Embed_Energy.append(Actual_Energy / Actual_Capacity)
    else:
        continue
print("****************************************************")
print(Embed_Energy)
print("****************************************************")
print(x_dic)
print("****************************************************")
print(y_dic)
x_result = x_dic[Embed_Energy.index(min(Embed_Energy))]
y_result = y_dic[Embed_Energy.index(min(Embed_Energy))]
print("****************************************************")
print(min(Embed_Energy))
print("****************************************************")
print(x_result, y_result)

# 广度搜索法
lower_bound = min(Embed_Energy)
resultx = []
resulty = []
print(lower_bound)


# 时间函数
def functionT(x, y, tpm, tpr):
    # 大/小/不
    sum = 0
    if len(x) == 0:
        return 0
    for index in range(len(x)):
        sum += tpr[index] * y[index] + tpm[index] * x[index]  # 维护总时间
    return sum


# 产线能耗计算
def functionE(x, y, m, n, ability, tstart, a, b):
    Machine_line = []
    for j in range(0, 9):
        my_machine = Machine(m[j], n[j], ability[j], x[j], y[j], tstart, a[j], b[j])
        Machine_line.append(my_machine)
    machines_station1 = [Machine_line[0], Machine_line[1]]
    machines_station2 = [Machine_line[2], Machine_line[3], Machine_line[4]]
    machines_station3 = [Machine_line[5], Machine_line[6], Machine_line[7], Machine_line[8]]
    F_Station1 = F_uni_par(machines_station1)
    F_Station2 = F_uni_par(machines_station2)
    F_Station3 = F_uni_par(machines_station3)
    P_Station1 = P_uni_par(machines_station1)
    P_Station2 = P_uni_par(machines_station2)
    P_Station3 = P_uni_par(machines_station3)
    Station1 = Station(F_Station1, P_Station1)
    Station2 = Station(F_Station2, P_Station2)
    Station3 = Station(F_Station3, P_Station3)
    Stations = [Station1, Station2, Station3]
    P = P_uni_ser(Stations)
    F = F_uni_ser(Stations)
    Actual_Capacity = Capacity(P, F, tstart, tend, 20, 50)
    Actual_Energy = energy(Machine_line, tstart, tend, 20, 30, 80)
    Embed_Energy = Actual_Energy / Actual_Capacity
    return Embed_Energy


# 补全函数
def bound(x, y, l, ismin):
    minE1 = y.copy()
    minE2 = x.copy()
    maxE1 = y.copy()
    maxE2 = x.copy()
    while len(minE1) < l:
        minE1.append(1)
        minE2.append(0)
        maxE1.append(0)
        maxE2.append(0)
    if (ismin):
        return minE1, minE2
    else:
        return maxE1, maxE2


class MyTree:
    def __init__(self, index, v1, v2, total, y, x):
        global lower_bound
        global resultx
        global resulty
        # 设备编号
        self.index = index
        # 大
        self.v1 = v1
        # 小
        self.v2 = v2
        self.resulty = []
        self.resultx = []
        print(self.index, self.v1, self.v2)
        temp1 = y.copy()
        temp2 = x.copy()
        if v1 is not None and self.index < total:
            temp1.append(v1)
            temp2.append(v2)
            print(temp1)
            print(temp2)
            boundMin1, boundMin2 = bound(temp1, temp2, total, True)
            boundMax1, boundMax2 = bound(temp1, temp2, total, False)
            # 时间
            print(functionT(temp1, temp2, tpm, tpr))
            # 能量
            print(boundMin1, boundMin2)
            print(boundMax1, boundMax2)
            print(functionE(boundMin1, boundMin2, m, n, ability, tstart, a, b))
            print(functionE(boundMax1, boundMax2, m, n, ability, tstart, a, b))
            print("-------------------------------------------")
            result_t = functionT(temp1, temp2, tpm, tpr)
            result_e = functionE(boundMin1, boundMin2, m, n, ability, tstart, a, b)
            if self.index < total and result_t <= T_limit and result_e <= lower_bound:
                self.aTree = MyTree(index + 1, 1, 0, total, temp1, temp2)
                self.bTree = MyTree(index + 1, 0, 1, total, temp1, temp2)
                self.cTree = MyTree(index + 1, 0, 0, total, temp1, temp2)
                if lower_bound > result_e:
                    lower_bound = result_e
                    resulty = boundMax1
                    resultx = boundMax2
        # 遍历
        elif self.index < total:
            self.aTree = MyTree(index + 1, 1, 0, total, temp1, temp2)
            self.bTree = MyTree(index + 1, 0, 1, total, temp1, temp2)
            self.cTree = MyTree(index + 1, 0, 0, total, temp1, temp2)


if __name__ == "__main__":
    time_start = time.time()
    array1 = []
    array2 = []
    root = MyTree(0, None, None, 9, array1, array2)
    print(lower_bound)
    print(resultx)
    print(resulty)
    print((time.time() - time_start))
    # array1 = [1, 1, 1, 1, 1, 1, 1, 1, 1]  # 大
    # array2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 小
    # at1 = [0]
    # at2 = [1]
    # print(functionE(array1, array2))
    # print(functionT(array1, array2))
    # print(bound(at1, at2, 9, True))
    # print(bound(at1, at2, 9, False))
