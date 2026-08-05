f :: Integer -> Integer
f n
  | n `mod` 2 == 0 = n - 1
  | otherwise            = 0

sumFun :: (Integer -> Integer) -> Integer -> Integer
sumFun f 0 = f 0
sumFun f n = f n + sumFun f (n - 1)

anyZero :: (Integer -> Integer) -> Integer -> Bool
anyZero f n
        | f n == 0 = True
        | n == 0  = False
        | otherwise = anyZero f (n-1)


maxFun :: (Integer -> Integer) -> Integer -> Integer 
maxFun f 0 = f 0 
maxFun f n = max (f n) (maxFun f (n-1))

insert :: Ord a => a -> [a] -> [a]
insert x [] = [x]
insert x (y:ys)
  | x <= y    = x : y : ys
  | otherwise = y : insert x ys

isort :: Ord a => [a] -> [a]
isort [] = []
isort (x:xs) = insert x (isort xs)

minimumm :: Ord a => [a] -> a
minimumm [x] = x
minimumm (x : xs) = min (x) (minimumm (xs))

delete :: Eq a => a -> [a] -> [a]
delete _ [] = []
delete x (y:ys)
  | x == y    = ys          
  | otherwise = y : delete x ys

ssort :: Ord a => [a] -> [a]
ssort [] = []
ssort xs = m : ssort (delete m xs)
  where m = minimumm xs

merge :: Ord a => [a] -> [a] -> [a]
merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y: ys)
    | x >= y = y : merge(x:xs) (ys) 
    | otherwise = x : merge (xs) (y:ys)

