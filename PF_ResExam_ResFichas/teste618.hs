--1. ["abc",[],"dce"]
--b) [[1],[2],[],[3],[4]]
--c) 10 
--d) [2,4,6,8]
--e) [1-0,3-3,5-6,7-9,9-12] == [1,0,-1,-2,-3]
--f) [6,8,10]
--g) [4,5,6]
--h) [(-1)ˆx * 2ˆx | x <- [1..]]
--i) 
--j) [a] -> a
--k) ([Bool],[Char])
--l)
--m)

--2)
avalia :: [Int] -> [Char]
avalia xs = [if x >= 15 then 'A' else 'R'| x <- xs]

injust :: [Int] -> Int 
injust xs = sum ([if x < 15 && x >= 10 then 1 else 0 | x <- xs])

--3)
repete :: a -> [[a]]
repete x = [] : map(x:) (repete x)

--4)