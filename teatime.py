#!/usr/bin/env python3

print("Решение задачки с перестановкой чайника и молочника")

# Размер "стола" (3x2 клетки)
n, m = 3, 2

# Максимальное число ходов
maxSteps = 45

# Минимальное число ходов решения для выхода из программы
minSteps = 17

# "Обрывать" поиск решения, если положение предметов на столе
# такое же как и в более ранних решениях (сущесвенно ускоряет поиск,
# но может находить не все альтернативные решения)
fast = True

# Исходное размещение предметов на столе
# 1,2,3-чашка (cup), T-чайник (tea), M-молочик (milk)
tab0 = (
  ("1", " ", "T"),
  ("2", "3", "M")  
)

# Функция проверки того, что мы "победили"
# (чайник с молочником должны быть на заданных местах)
def check(tab):
  return tab[0][2] == "M" and \
         tab[1][2] == "T"

# Функция распечатки состояния предметов на столе
def show(tab):
  for row in tab:
    for item in row:
      print("", item, end="")
    print()
  print()

# Функция копирования состояния предметов на столе
def copy(tab):
  new = []
  for row in tab:
    new.append(list(row))
  return new

# Функция преобразования состояния в строку (для хэширования)
def thash(tab):
  retv = ""
  for row in tab:
    for item in row:
      retv += item
  return retv

# Функция сравнения состояний предметов на столе
def cmp(tab1, tab2):
  if tab1 == None or tab2 == None:
    return False
  for i in range(len(tab1)): # 0..m-1
    for j in range(len(tab1[i])): # 0..n-1
      if tab1[i][j] != tab2[i][j]:
        return False # различие найдено
  return True # состояния совпадают

# Сделать один ход (поменять сдвинуть предмет)
# (i1, j1) - старая позиция предмета, Ii2, j2) - свободная клетка
def step(tab, i1, j1, i2, j2):
  tab = copy(tab)
  tab[i2][j2] = tab[i1][j1]
  tab[i1][j1] = " "
  return tab

# Функция вычисления возможных состояний для следующего хода
def find(tab):
  m = len(tab)    - 1 # 2-1=1
  n = len(tab[0]) - 1 # 3-1=2 

  # Проверить "углы стола"
  # (при свободной угловой клетке, возможно два хода)
  if tab[0][0] == " ": # свободен верхний левый угол
    return step(tab, 0, 1, 0, 0), \
           step(tab, 1, 0, 0, 0)
  elif tab[0][n] == " ": # свободен верхний правый угол
    return step(tab, 0, n-1, 0, n), \
           step(tab, 1, n,   0, n)
  elif tab[m][0] == " ": # свободен нижний левый угол
    return step(tab, m-1, 0, m, 0), \
           step(tab, m,   1, m, 0)
  elif tab[m][n] == " ": # свободен нижний правый угол
    return step(tab, m-1, n, m, n), \
           step(tab, n-1, m, m, n)

  # Проверить центральные верхние и нижний клетки
  # (возможно три хода)
  if tab[0][1] == " ":
    return step(tab, 0, 0, 0, 1), \
           step(tab, 0, 2, 0, 1), \
           step(tab, 1, 1, 0, 1)
  elif tab[1][1] == " ":
    return step(tab, 1, 0, 1, 1), \
           step(tab, 1, 2, 1, 1), \
           step(tab, 0, 1, 1, 1)

  # Проверять края и "середину" не будем - это не пятнашки
  print("error") #этого не может быть!

# Функция вычисления массива следующих состояний
# с исключением "обратных" ходов (prev)
def child(tab, prev):
  c = []
  for t in find(tab):
    # исключить шаги назад && исключить ходы возращяющие нас в начало игры
    if not cmp(t, prev) and not cmp(t, tab0):
      c.append(t)
  return c

# Узел дерева всевозможных ходов
class Node:
  # Создать узел дерева всевозможных ходов
  def __init__(self, tab, parent):
    self.tab    = tab    # таблица состояния игрового поля
    self.parent = parent # родительский узел
    self.child  = []     # дочерние узлы (массив)

# Создать первый узел дерева всевозможных ходов
node0 = Node(tab0, None)

# Массивы узлов возможных состояний для разного числа ходов
# (с каждых ходом возможных узлов состояний все больше)
level = [[node0]]

# Словарь с указанием узла для каждого состояний
dic = {thash(tab0): node0}

# Построим дерево для всевозможных ходов
# (функция возвращает узлы дерева в состоянии решения)
def run(minSteps, maxSteps):
  for i in range(len(level), maxSteps + 1):
    oldLevel = level[i-1]
    newLevel = []
    result = [] # список найденных решений (узлов)
    for j in range(len(oldLevel)): # цикл по всевозможным решения предыдущего шага
      node = oldLevel[j]
      prev = None
      if node.parent != None:
        prev = node.parent.tab
      node.child = child(node.tab, prev)
      for tab in node.child: # цикл по всем следующим состояниям
        newNode = Node(tab, node)
        if check(tab): # решение найдено
          result.append(newNode)
        if fast: # поиск только "коротких" решений
          h = thash(tab)
          if not h in dic: # новое состояние
            newLevel.append(newNode)
            dic[h] = newNode
        else:
          newLevel.append(newNode)
    level.append(newLevel)
    print(str(i) + "-" + str(len(newLevel)) + "->" + str(len(result)))
    if i >= minSteps:
      return result
  return []

# Вывести последовательность ходов
def trace(node):
  path = [node]
  while node.parent != None:
    node = node.parent
    path.append(node)
  cnt = 0
  for i in range(len(path) - 1, -1, -1):
    print("#" + str(cnt) + "-" + str(len(path[i].child)) + ":")
    show(path[i].tab)
    cnt += 1

# Выполнить поиск решений
result = run(minSteps, maxSteps)

# Число выводимых решений (ограничено)
resNum = min(3, len(result))

# Вывести найденные решения (с учётом ограничений)
for i in range(resNum):
  print("-----")
  trace(result[i])

