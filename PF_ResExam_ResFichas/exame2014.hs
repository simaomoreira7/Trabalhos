--1)
--a) [1,2]
--b) [1,3,5,7] -> [7,5,3,1]
--c) [1,2,3]
--d) 4
--e) ['c','d','r']
--f) [(2,'a'),(3,'b'),(4,'c')]
--g) 17
--h) [(Int,Int)]
--i) [[a]-> ([a] -> ([a] -> [a]))]
--j) [a] -> [a]

--2) 
transforma :: String -> String
transforma [] = []
transforma (x:xs) 
    |x == 'a' || x == 'e' || x == 'i' || x == 'o' || x == 'u' = x:'p':x: transforma xs
    |otherwise = x : transforma xs

--3)
subidas :: [Float] -> Int 
subidas [] = 0
subidas [_] = 0 
subidas (x:y:xs) 
    | x < y = 1 + subidas (y:xs)
    | otherwise = 0 + subidas (y:xs)

--4)
--a)
data Arv a = F | N a (Arv a) (Arv a)

alturas :: Arv a -> Arv Int
alturas F = 1
