--Questão1)

factorial :: Int -> Int 
factorial 0 = 1
factorial n = n * factorial (n - 1)

approxE :: Int -> Double 
approxE k = sum [1 / fromIntegral(factorial x) | x <- [0..k]]

--Questão2)

agrupar :: Eq a => [a] -> [[a]]
agrupar [] = []
agrupar [x] = [[x]]
agrupar (x:y:xs)
    | x == y    = (x : head grupos) : tail grupos
    | otherwise = [x] : grupos
    where
        grupos = agrupar (y:xs)

--Questão3)

member :: Ord a => a -> Set a -> Bool
