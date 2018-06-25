CREATE DATABASE nutripower CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE nutripower.alimento (
id_alimento int PRIMARY KEY,
nome varchar(200),
umidade varchar(45),
Kcal varchar(45),
Kj varchar(45),
proteina varchar(45),
lipidio varchar(45),
colesterol varchar(45),
carboidrato varchar(45),
fibra_Alimentar varchar(45),
cinzas varchar(45),
calcio varchar(45),
magnezio varchar(45),
manganes varchar(45),
fosforo varchar(45),
ferro varchar(45),
sodio varchar(45),
potacio varchar(45),
cobre varchar(45),
zinco varchar(45),
retinol varchar(45),
re varchar(45),
rae varchar(45),
tiamina varchar(45),
riboflavina varchar(45),
piridoxina varchar(45),
niacina varchar(45),
vitamina_c varchar(45)
);

CREATE TABLE nutripower.cidade (
id_cidade int PRIMARY KEY AUTO_INCREMENT,
id_estado int,
nome_cidade varchar(200)
);

CREATE TABLE nutripower.endereco (
id_endereco int PRIMARY KEY AUTO_INCREMENT,
id_pais int,
id_estado int,
id_cidade int,
id_bairro int,
cep int,
nome_rua varchar(200),
numero_casa int,
complemento varchar(200),
FOREIGN KEY(id_cidade) REFERENCES nutripower.cidade (id_cidade)
);

CREATE TABLE nutripower.bairro (
id_bairro int PRIMARY KEY AUTO_INCREMENT,
id_cidade int,
nome_bairro varchar(200),
FOREIGN KEY(id_cidade) REFERENCES nutripower.cidade (id_cidade)
);

CREATE TABLE nutripower.pais (
id_pais int PRIMARY KEY AUTO_INCREMENT,
nome_pais varchar(200)
);

CREATE TABLE nutripower.nutricionista (
id_nutricionista int PRIMARY KEY AUTO_INCREMENT,
nome varchar(200),
senha varchar(45),
foto varchar(200)
);


CREATE TABLE nutripower.consulta (
id_consulta int PRIMARY KEY AUTO_INCREMENT,
id_paciente int,
id_avaliacao int,
id_dieta int,
id_nutricionista int,
objetivo varchar(450),
proxima_consulta varchar(200),
data date,
FOREIGN KEY(id_nutricionista) REFERENCES nutripower.nutricionista (id_nutricionista)
);


CREATE TABLE nutripower.modelos_refeicao (
id_modelo_refeicao int PRIMARY KEY AUTO_INCREMENT,
horario_refeicao varchar(45),
nome_refeicao varchar(200),
objetivo_refeicao varchar(200)
);

CREATE TABLE nutripower.alimentos_modelo_refeicao (
id_alimentos_modelo_refeicao int PRIMARY KEY AUTO_INCREMENT,
id_alimento int,
id_modelo_refeicao int,
FOREIGN KEY(id_modelo_refeicao) REFERENCES nutripower.modelos_refeicao(id_modelo_refeicao),
FOREIGN KEY(id_alimento) REFERENCES nutripower.alimento (id_alimento)
);

CREATE TABLE nutripower.refeicao (
id_refeicao int PRIMARY KEY AUTO_INCREMENT,
id_alimentos_refeicao int,
horario_refeicao varchar(45),
nome_refeicao varchar(200)
);

CREATE TABLE nutripower.alimentos_refeicao (
id_alimentos_refeicao int PRIMARY KEY AUTO_INCREMENT,
id_alimento int,
id_refeicao int,
FOREIGN KEY(id_refeicao) REFERENCES nutripower.refeicao (id_refeicao),
FOREIGN KEY(id_alimento) REFERENCES nutripower.alimento (id_alimento)
);

CREATE TABLE nutripower.dieta (
id_dieta int PRIMARY KEY AUTO_INCREMENT,
nome_dieta varchar(200),
objetivo varchar(200)
);

CREATE TABLE nutripower.refeicoes_dieta (
id_refeicoes_deita int PRIMARY KEY AUTO_INCREMENT,
id_refeicao int,
id_dieta int,
FOREIGN KEY(id_dieta) REFERENCES nutripower.dieta (id_dieta)
);



CREATE TABLE nutripower.paciente (
id_paciente int PRIMARY KEY AUTO_INCREMENT,
id_endereco int,
peso double,
sexo char,
cpf varchar(45),
altura double,
telefone varchar(45),
nome varchar(200),
idade int,
email varchar(200),
atividade_fisica varchar(200),
foto varchar(200),
FOREIGN KEY(id_endereco) REFERENCES nutripower.endereco (id_endereco)
);


CREATE TABLE nutripower.avaliacao_fisica (
id_avaliacao int PRIMARY KEY AUTO_INCREMENT,
id_paciente int,
porcentagem_gordura double,
metabolismo_basal double,
porcentagem_massa_muscular double,
altura double,
imc double,
porcentagem_massa_magra double,
pressao double,
objetivo varchar(450),
data date,
peso double,
observacoes varchar(450),
FOREIGN KEY(id_paciente) REFERENCES nutripower.paciente (id_paciente)
);

CREATE TABLE nutripower.estado (
id_estado int PRIMARY KEY AUTO_INCREMENT,
id_pais int,
nome_estado varchar(200),
FOREIGN KEY(id_pais) REFERENCES pais (id_pais)
);

ALTER TABLE nutripower.refeicoes_dieta ADD FOREIGN KEY(id_refeicao) REFERENCES nutripower.refeicao (id_refeicao);
ALTER TABLE nutripower.cidade ADD FOREIGN KEY(id_estado) REFERENCES nutripower.estado (id_estado);
ALTER TABLE nutripower.endereco ADD FOREIGN KEY(id_pais) REFERENCES nutripower.pais (id_pais);
ALTER TABLE nutripower.endereco ADD FOREIGN KEY(id_estado) REFERENCES nutripower.estado (id_estado);
ALTER TABLE nutripower.endereco ADD FOREIGN KEY(id_bairro) REFERENCES nutripower.bairro (id_bairro);
ALTER TABLE nutripower.consulta ADD FOREIGN KEY(id_paciente) REFERENCES nutripower.paciente (id_paciente);
ALTER TABLE nutripower.consulta ADD FOREIGN KEY(id_avaliacao) REFERENCES nutripower.avaliacao_fisica (id_avaliacao);
ALTER TABLE nutripower.consulta ADD FOREIGN KEY(id_dieta) REFERENCES nutripower.dieta (id_dieta);
