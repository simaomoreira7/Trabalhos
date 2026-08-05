--1)
-- words divide em palavras; map toLower deixa a palavra com cada caracter em minuscula 
-- se eu tivesse na aline a map(toLower . words) o que é que aconteceria?
--Resposta : C
--b) 
-- Não percebi o porquê que a opção B não pode ser 
-- Resposta : A
--c)
-- Resposta : B
--d) 
--Não percebi a alinea d)
-- Resposta : A
--e)
-- Polimórfica -> usa vários tipos ; Ordem Superior -> Recebe ou retorna funções
-- Resposta : C
--f) 
-- não percebi o que está a acontecer no f 
-- Resposta : C

--2)
--a) [1,2,0,3,0]
--b) [(-1)^x / 2^x | x <-[0..]]
--c) Eq a => [a] -> Bool
--d) data Tree = Leaf | Node Tree Int Tree
--e) [Int] -> [Int]
--f) 6

--3)
pontuacao :: [(String,Int,Int,Int)] -> [(String, Int)]
pontuacao = map (\(nome,v,e,_) -> (nome , v*3 + e*1))

njogos :: Int -> [(String, Int, Int, Int)] -> Bool
njogos n = all(\(_,v,e,d) -> v+e+d == n)


--Questões)
-- se eu tivesse na aline a map(toLower . words) o que é que aconteceria?
-- Não percebi o porquê que a opção B não pode ser 
-- Não percebi a alinea d)
-- o que é polimorfica e de ordem superior qual é a diferença e o que é que cada uma faz?
-- não percebi o que está a acontecer no f 
