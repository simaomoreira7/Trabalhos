data Tree a = Empty | Node a (Tree a) (Tree a)

--8.1)
sumTree :: Num a => Tree a -> a 
sumTree Empty = 0 
sumTree (Node x left right) = x + sumTree left + sumTree right

--8.2)
list :: Tree a -> [a]
list Empty = []
list (Node x left right) = list right ++ [x] ++ list left

--8.3)
level :: Int -> Tree a -> [a]
level _ Empty = []
level 0 Node (x _ _) = [x]
level n (Node _ left right) = level (n-1) left ++ level (n-1) right
