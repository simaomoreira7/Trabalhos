--6)
--6.1)
factorial = [f x | x <- [0..]]
    where 
        f 0 = 1
        f n = n * f (n-1)

fibonaccis = [g x | x <- [0..]]
    where 
        g 0 = 0
        g 1 = 1
        g n = g (n-1) + g (n-2)

--6.2)
merge :: Ord a => [a] -> [a] -> [a]
merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys)
    | x < y     = x : merge xs (y:ys)
    | x > y     = y : merge (x:xs) ys
    | otherwise = x : merge xs ys 

--6.3)
sequencia = [1..]

sumss :: [Int] -> [Int]
sumss sequencia = [h x | x <- [0..]]
    where 
        h 0 = 0 
        h x = sequencia !! (x-1) + h(x-1)

--6.4)
