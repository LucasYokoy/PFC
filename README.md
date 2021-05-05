# PFC
Projeto final de curso
OBSERVAÇÕES SOBRE A IMPLEMENTAÇÃO
- Sobre a limpeza do dataset
	- Primeiramente, foram desenvolvidos dois métodos: um que extrai dados de PDFs e outro que extraí dados de documentos de word DOCX.
	- Apesar de ambos serem utilizaveis e funcionais, é preferível que os documentos sejam dados no formato DOCX para evitar poluição.
	- Todos os métodos desenvolvidos utilizam expressões regulares e substituição de strings para eliminar alguns padrões comuns. Os padrões eliminados foram:
		- A enumeração das linhas, pois não carrega nenhuma informação útil sobre o conteúdo do documento.
		- \n os caracteres new line foram limpos devido a possibilidade de eles se juntarem às palávras anteriores ou seguintes, produzindo palávras novas que seriam difíceis de filtrar.
		- Todos os documentos possuem uma lista de participantes no final. Essa lista, inicialmente foi mantida, supondo-se que ela continha dados relevantes, como os nomes dos participantes. Mas posteriormente, concluíu-se que ela não era relevante por que os nomes dos participantes estão contidos no corpo do texto.
	- Sobre o modelo:
		- Foram utilizados diversos modelos diferentes, mas o que funcionou melhor foi o modelo  pierreguillou/bert-base-cased-squad-v1.1-portuguese.
		- O modelo foi pré treinado em português no dataset SQUAD. Acreditavamos que seria necessário treinar o modelo para a aplicação específica, mas as respostas que ele produzia sem treinamento já eram satisfatórias.
		- Treinamento adicional poderá ser feito usando as perguntas e respostas adquiridas em produção.
	- Sobre a construção do corpus, e processo de perguntas e respostas
		- Inicialmente, tentou-se colocar todo o corpus em um único documento, e alimentar o modelo de uma vez só. Ficou rapidamente evidente, que esta solução era inviável por vários motivos:
			- O modelo não foi capaz de compreender que cada ata se tratava de um documento distinto, em seu próprio contexto isolado (o que era de se esperar).
			- Devido a alta complexidade, e falta de relação entre os textos, demorou-se quase 40 minutos para produzir uma resposta, alocando-se mais de 20 GB de memória RAM, e a resposta estava incorreta.
		- A segunda tentativa foi colocar os documentos em uma lista, e fazer o modelo analisar separadamente.
		- Inicialmente, tentamos usar o modelo em CPU. Isso se mostrou inviável por demorar tempo demais para responder qualquer pergunta (40 minutos, como dito anteriormente).
	- Sobre a interface e a experiência de usuário