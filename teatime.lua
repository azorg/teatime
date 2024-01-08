#!/bin/env lua

print "Решение задачки с перестановкой чайника и молочника"

-- Размер "стола" (3x2 клетки)
n, m = 3, 2

-- Максимальное число ходов
steps = 100

-- Минимальное число ходов решения
minSteps = 17

-- Исходное размещение предметов на столе
-- C-чашка (cup), T-чайник (tea), M-молочик (milk)
tab0 = {
  { "C", " ", "T" },
  { "C", "C", "M" }  
}

-- Функция проверки того, что мы "победили"
-- (чайник с молочником должны быть на заданных местах)
function check(tab)
  return tab[1][3] == "M" and -- молочник на месте
         tab[2][3] == "T"     -- чайник на месте
end

-- Функция распечатки состояния предметов на столе
function show(tab)
  if tab == nil then return end
  for i = 1, #tab do -- 1..m
    for j = 1, #tab[i] do -- 1..n
      io.write(" ", tab[i][j])
    end
    print()
  end
  print()
end

-- Функция копирования состояния предметов на столе
function copy(tab)
  local new = {}
  for i = 1, #tab do -- 1..m
    new[i] = {}
    for j = 1, #tab[i] do -- 1...n
      new[i][j] = tab[i][j]
    end
  end
  return new
end

-- Функция сравнения состояний предметов на столе
function cmp(tab1, tab2)
  if tab1 == nil or tab2 == nil then
    return false
  end
  for i = 1, #tab1 do -- 1..m
    for j = 1, #tab1[i] do -- 1...n
      if tab1[i][j] ~= tab2[i][j] then
		return false -- различие найдено
	  end
    end
  end
  return true -- состояния совпадают
end

-- Сделать один ход (поменять сдвинуть предмет)
function step(old, i1, j1, i2, j2)
  local tab = copy(old)
  tab[i2][j2] = tab[i1][j1]
  tab[i1][j1] = " "
  return tab
end 

-- Функция вычисления возможных состояний для следующего хода
function find(tab)
  local m = #tab    -- 2
  local n = #tab[1] -- 3

  -- Проверить "углы стола"
  -- (при свободной угловой клетке, возможно два хода)
  if tab[1][1] == " " then -- свободен верхний левый угол
    return step(tab, 1, 2, 1, 1),
           step(tab, 2, 1, 1, 1)
  elseif tab[1][n] == " " then -- свободен верхний правый угол
    return step(tab, 1, n-1, 1, n),
           step(tab, 2, n, 1, n)
  elseif tab[m][1] == " " then -- свободен нижний левый угол
    return step(tab, m-1, 1, m, 1),
           step(tab, m, 2, m, 1)
  elseif tab[m][n] == " " then -- свободен нижний правый угол
    return step(tab, m-1, n, m, n),
           step(tab, n-1, m, m, n)
  end

  -- Проверить центральные верхние и нижний клетки
  -- (возможно три хода)
  if tab[1][2] == " " then
    return step(tab, 1, 1, 1, 2),
           step(tab, 1, 3, 1, 2),
           step(tab, 2, 2, 1, 2)
  elseif tab[2][2] == " " then
    return step(tab, 2, 1, 2, 2),
           step(tab, 2, 3, 2, 2),
           step(tab, 1, 2, 2, 2)
  end

  -- Проверять края и "середину" не будем - это не пятнашки
  print "error" -- этого не может быть!
end

-- Функция вычисления массива следующих состояний
-- с исключением "обратных" ходов (prev)
function child(tab, prev)
  local i = 0
  local c = {}
  for _, t in pairs{find(tab)} do
    if t ~= nil and         -- ход найден
       not cmp(t, prev) and -- исключить шаги назад
       not cmp(t, tab0)     -- ход не возращяет нас в начало игры
    then
      i = i + 1
      c[i] = t
    end
  end
  return c
end

-- Создать узел дерева всевозможных ходов
function new(tab, parent)
  return {
    tab    = tab,    -- таблица состояния игрового поля
    parent = parent, -- родительский узел
    child  = {}      -- дочерние узлы (массив)
  }
end 

-- Создать первый узел дерева всевозможных ходов
node0 = new(tab0, nil)

-- Массивы узлов возможных состояний для разного числа ходов
-- (с каждых ходом возможных узлов состояний все больше)
level = {[0] = {node0}}

-- Словарь с указанием узла для каждого состояний
dict = {[tab0] = node0}

-- Построим дерево для всевозможных ходов
-- (функция возвращает узел дерева в состоянии решения)
function run(steps)
  for i = 1, steps do
    print(i)
    newLevel = {}
    for _, node in pairs(level[i-1]) do
      local prev = tab
      if node.parent ~= nil then
        prev = node.parent.tab
      end
      node.child = child(node.tab, prev)
      for j, tab in pairs(node.child) do
        if dict[tab] == nil then -- новое состояние
          newNode = new(tab, node)
          newLevel[#newLevel + 1] = newNode
          dict[tab] = newNode
          if check(tab) then
            print "Bingo!"
            if i >= minSteps then
              return newNode
            end
          end
        end
      end
    end -- for node
    if #newLevel == 0 then
      print "Finish!"
      return node
    end
    level[i] = newLevel
  end -- for i
  return node0
end

-- Вывести последовательность ходов
function trace(node)
  local path = {node}
  while node.parent ~= nil do
    node = node.parent
    path[#path + 1] = node
  end
  local cnt = 0
  for i = #path, 1, -1 do
    print("#" .. cnt .. "-".. #path[i].child.. ":")
    show(path[i].tab)
    cnt = cnt + 1
  end
end

-- Выполнить поиск решения
node = run(steps)

-- Вывести решение
print()
trace(node)
