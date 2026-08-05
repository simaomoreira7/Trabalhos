data Arv a = Folha | No a (Arv a) (Arv a)
contem :: Eq a => a -> Arv a -> Bool
contem _ Folha = False
contem n (No x esq dir)
    | n == x = True
    | otherwise = contem n esq || contem n dir

somaNos :: Num a => Arv a -> a 
somaNos Folha = 0
somaNos (No x esq dir) = x + somaNos esq + somaNos dir