--1)
--a) [[],[],[],[]]
--b) 4
--c) [0, 0, 0, 1, 1, 1, 1, 2, 2, 2]
--d) [1,3,9,27,81]
--e) [4,8]
--f) [2, 4,6,8,10,12,14,16,18,20]
--g) [if even x then 2*x else 2ˆx-1 | x <-[0..]]
--h) False
--i) [Int -> Bool]
--j) [Char] -> Int 
--k) Arv = Vazia | No (Arv) a (Arv)

--2)
imparDiv3:: [Int] -> Bool
imparDiv3 xs = and [ odd x | x <- xs, x ‘mod‘ 3 == 0]

impardiv3:: [Int] -> Bool
impardiv3 = (all odd) . (filter (\x -> x ‘mod‘ 3 == 0))

--4)
javardice = [f x | x <- [1..]]
    where 
        f 1 = 1
        f n = 2 * f(n-1) + n + 1 
--5) 
duplicada :: Eq a => [a] -> Bool
duplicada [] = True
duplicada [_] = False
duplicada (x:y:xs)
    | x == y = duplicado xs  
    | otherwise = False 

duplica :: [a] -> [a]
duplica xs = [y | x <- xs, y <-[x,x]]

--6) 
data Arv a = Folha a | No (Arv a) (Arv a)

emOrdem :: Arv a -> [a]
emOrdem (Folha x) = [x]
emOrdem (No esquerda direita) = emOrdem esquerda ++ emOrdem direita


