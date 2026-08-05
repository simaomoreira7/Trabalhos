-- === Folha rápida: Funções Padrão do Prelude em Haskell ===

-- 1. Operações com listas e números

sum :: (Num a) => [a] -> a
-- Soma todos os elementos da lista
-- Exemplo: sum [1,2,3] == 6

product :: (Num a) => [a] -> a
-- Multiplica todos os elementos da lista
-- Exemplo: product [2,3,4] == 24

maximum :: (Ord a) => [a] -> a
-- Retorna o maior elemento da lista (lista não vazia)
-- Exemplo: maximum [1,5,3] == 5

minimum :: (Ord a) => [a] -> a
-- Retorna o menor elemento da lista (lista não vazia)
-- Exemplo: minimum [1,5,3] == 1

-- 2. Funções de transformação e filtro

map :: (a -> b) -> [a] -> [b]
-- Aplica uma função a cada elemento da lista
-- Exemplo: map (*2) [1,2,3] == [2,4,6]

filter :: (a -> Bool) -> [a] -> [a]
-- Retorna só os elementos que satisfazem o predicado
-- Exemplo: filter even [1..5] == [2,4]

-- 3. Funções de combinação

zip :: [a] -> [b] -> [(a,b)]
-- Combina duas listas em pares
-- Exemplo: zip [1,2] ['a','b'] == [(1,'a'),(2,'b')]

zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
-- Aplica uma função combinando os elementos de duas listas
-- Exemplo: zipWith (+) [1,2] [3,4] == [4,6]

-- 4. Funções de dobra (folds)

foldr :: (a -> b -> b) -> b -> [a] -> b
-- Aplica função dobrando da direita para a esquerda
-- Exemplo: foldr (+) 0 [1,2,3] == 6

foldl :: (b -> a -> b) -> b -> [a] -> b
-- Aplica função dobrando da esquerda para a direita
-- Exemplo: foldl (+) 0 [1,2,3] == 6

-- 5. Outras funções úteis

length :: [a] -> Int
-- Retorna o tamanho da lista
-- Exemplo: length [1,2,3] == 3

null :: [a] -> Bool
-- Retorna True se a lista é vazia, False caso contrário
-- Exemplo: null [] == True

reverse :: [a] -> [a]
-- Inverte a lista
-- Exemplo: reverse [1,2,3] == [3,2,1]

-- 6. Operadores básicos para comparações e aritmética

(==) :: Eq a => a -> a -> Bool
-- Verifica igualdade

(/=) :: Eq a => a -> a -> Bool
-- Verifica desigualdade

(<), (<=), (>), (>=) :: Ord a => a -> a -> Bool
-- Operadores de comparação

(+) :: Num a => a -> a -> a
(-) :: Num a => a -> a -> a
(*) :: Num a => a -> a -> a
-- Operações aritméticas básicas

-- 7. Funções de geração de listas

replicate :: Int -> a -> [a]
-- Gera lista com elemento repetido n vezes
-- Exemplo: replicate 3 'a' == "aaa"

take :: Int -> [a] -> [a]
-- Pega os primeiros n elementos
-- Exemplo: take 2 [1,2,3] == [1,2]

drop :: Int -> [a] -> [a]
-- Remove os primeiros n elementos
-- Exemplo: drop 2 [1,2,3] == [3]

-- 8. Funções lógicas

not :: Bool -> Bool
-- Negação lógica

(&&) :: Bool -> Bool -> Bool
-- E lógico

(||) :: Bool -> Bool -> Bool
-- Ou lógico

-- ======= FIM DA FOLHA =======
