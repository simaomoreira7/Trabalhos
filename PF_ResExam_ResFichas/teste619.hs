--1)
--a) 4
--b) [[1,2],[3]]
--c) [1+10,3+9,5+8,7+7,9+6]
--d) ((2*5)*4)*3*2*1 == 240
--e) []
--f) False
--g) [(1,1),(4,4),(9,7),(16,10),(25,13),(36,16)]
--h) [(x,y) | x <- [1,3..], y <- [10,8..] | x + y == 11]
--i) [5,4,3,2,1]
--j) Num a => a -> a 
--k) [(Bool -> Bool) -> [Bool] -> [Bool]]
--l) data Arv a = F a | N (Arv a) (Arv a)
--m) (a -> Bool) -> [a] -> [a]

--2.)
notaf :: Num a => [a] -> [a] -> a
notaf xs ys = sum (zipWith (*) xs ys)

--2.b)
rfc :: [[Double]] -> Int
rfc alunos = length (filter temNotaBaixa alunos)
  where
    temNotaBaixa notas = any (< 8.0) notas

--3)
type Vert = Int
type Graph = [(Vert, Vert)]

transitiva :: Graph -> Bool
transitiva g = all verifica g
  where
    verifica (v1, v2) = all (\(_, v3) -> (v1, v3) `elem` g) 
                             [(x, y) | (x, y) <- g, x == v2]

--4)
iterate :: (a -> a) -> a -> [a]
iterate f x = x : [ y | y <- iterate f (f x) ]

--5.a)
deleteNth :: Int -> [a] ->[a]
deleteNth _ [] = []
deleteNth n xs 
    | n <= 0 = xs 
    | otherwise = take (n-1) xs ++ deleteNth n (drop n xs)

--b)
deleteNth :: Int -> [a] -> [a]
deleteNth n xs = [ x | (i, x) <- zip [1..] xs, i `mod` n /= 0 ]

--6

somaArv:: Arv -> Int
