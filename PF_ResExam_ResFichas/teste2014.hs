--1) 
--a) [[1,2],[3],[5],[]] -> 4
--b) [[],[3],[5,2]] -> 3
--c) 20 + 2 = 22
--d) [True, True, False, False, False]
--e) 26
--f) [(2,1),(3,2),(4,3)]
--g) [(x,2^y)| x <- [1,3..], y <- [1..]]
--h) [2,4,2,10,12]
--i) [Int -> Bool]
--j) Num a => a -> a 
--k) Arv = Folha Int| Node Arv Arv
--l) [a] -> [a] -> a

--2)
nafrente :: Char -> [[Char]] -> [[Char]]
nafrente x listas = [x : lista | lista <- listas]

ocorreN :: Char -> [[Char]] -> Int-> [[Char]]
nafrente x l n = length (filter( == x) l) == n

--3)
subs :: [Int] -> [[Int]]
subs [] = [[]]
subs (x:xs) = subs xs ++ map (x:) (subs xs)

subsAsc :: [Int] -> [[Int]]
subsAsc [] = [[]]
subsAsc (x:xs) = subsAsc xs ++ map (x:) (filter (all (<= x)) (subsAsc xs))

--5)
--a)
data ArvT a = Folha a | Node (Arvt a) (Arvt a) (Arvt a)
--b)
nelementos :: ArvT a -> Int
nelementos (Folha _) = 1  -- Uma folha conta como 1 elemento
nelementos (No esq centro dir) = nelementos esq + nelementos centro + nelementos dir

--c)
mapTree :: (a -> b) -> ArvT a -> ArvT b
mapTree f (Folha x) = Folha (f x)  -- Aplica `f` ao valor da folha
mapTree f (No esq centro dir) = No (mapTree f esq) (mapTree f centro) (mapTree f dir)