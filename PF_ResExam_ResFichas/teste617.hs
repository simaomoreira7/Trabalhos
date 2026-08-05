--1)
--a) [[1,2],[3],[5],[]] == 4
--b)[[],[3],[5,2]] == []
--c) 22
--d)[T,T,T,F,F]
--e) 26
--f) (2,1),(3,2),(4,3)
--g) [(x,2^(x `div` 2 +1)) | x <- [1,3..]]
--h) [2,4,2,10,12]
--i) [Int -> Bool]
--j) Num a => a -> a
--k) Folha a | No Arv  Arv 
--l) Num a => [a] -> [a] -> a
 
--2)
nafrente :: Char -> [[Char]] -> [[Char]]
nafrente n xs = [ n: x | x <- xs]

ocorreN :: Eq a => Int -> a -> [a] -> Bool
ocorreN n x l = length (filter (== x) l) == n

--3)
subs :: [a] -> [[a]]
subs [] = [[]]
subs (x:xs) = smap (x:) (subs xs) ++  subs xs 

subsAsc :: Ord a => [a] -> [[a]]
subsAsc [] = [[]]
subsAsc (x:xs) = [] : [x:ys | ys <- subsAsc xs, null ys || x <= head ys] ++ tail (subsAsc xs)


--5)
data ArvT a = Folha a | No (ArvT a) (ArvT a) (ArvT a)
arv = No (Folha 1) (No(Folha 4)(Folha 5) (Folha 8)) (Folha 9)