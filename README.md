# Vendas Rossmann

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/rossmann-logo.png?raw=true)

## 1. Problema de Negócio
O CFO da empresa fez uma reunião com todos os Gerentes de Loja e pediu para que cada um deles trouxesse uma previsão diária das próximas 6 semanas de vendas.

Depois dessa reunião, todos os Gerentes de Loja entraram em contato com você, requisitando uma previsão de vendas de sua loja. O seu trabalho é fazer essa previsão.

## 2. Premissas do negócio

* Apenas lojas abertas serão consideradas.
* Apenas lojas com vendas serão levadas em conta.

### 2.1 Descrição dos atributos

* **Id** - id da loja
* **Store** - Identificação única para a loja
* **Sales** - O quanto de venda aquele produto teve diariamente
* **Customers** - Número de clientes que visitaram a loja naquele dia
* **Open** - Indicador se a loja está aberta ou fechada (0 = fechada, 1 = aberta)
* **StateHoliday** - Indica se naquele dia está ocorrendo algum feriado do estado
* **SchoolHoliday** - Indica se naquele dia está ocorrendo algum feriado escolar
* **StoreType** - O tipo de loja, divididos em a,b,c e d.
* **Assortment** - A disposição dos produtos em cada loja, divididos em 3 tipos, a = basic, b = extra e c = extended
* **CompetitionDistance** - Distancia (em metros) para o competidor mais próximo
* **CompetitionOpenSince[Month/Year]** - Mês e ano que a competição surgiu. Se eu tenho uma loja agora, daqui a 6 meses abre uma loja nova, tem a data que a competição de iniciou.
* **Promo** - Indicativo se a loja está participando de uma promoção.
* **Promo2** - É uma extensão da promoção. As lojas fazem promoções e outras extendem essa promoção por mais tempo. 0 = loja não participando, 1 = loja participando
* **Promo2Since[Month/Year]** - Indica o tempo que a loja ficou na promoção extendida.
* **PromoInterval** - Intervalo que essas promoções acontecem.

## 3. Planejamento da Solução

A partir do pedido do CFO e da análise dos dados é possível observar que esta é um claro problema de predição, que será usado um modelo de Machine Learning para solucionar. Depois disso será feito o deploy do modelo no Heroku e poderá ser acessado em qualquer telefone com acesso ao aplicativo Telegram.

Será utilizado o método cíclico CRISP-DS (Cross-Industry Process - Data Science) , que é um metodo de gerenciamento de projetos para ciência de dados. A vantagem deste método é que entrega-se valor de uma forma mais rápida. O processo consiste nas seguintes etapas:

**0.** Aquisição dos Dados
* Neste nosso projeto, os dados vieram do Kaggle: https://www.kaggle.com/c/rossmann-store-sales/data

**1.** Descrição dos Dados
* A partir de métricas estatísticas encontra-se valores mínimos, máximos, outliers, médias, dados faltantes entre outros problemas que será encontrado durante o projeto.

**2.** Engenharia de Atributos
* Nesta etapa será encontrado novos atributos a partir das variáveis originais, de forma que melhore a análise exploratória de dados. Além disso, cria-se hipóteses que serão validadas (ou rejeitadas) na análise.

**3.** Filtragem de Dados
* A principal motivação para realizar este passo é por restrição de negócios. Alguns atributos pode impactar no resultado, porém, não estarão disponíveis antes do modelo em produção.

**4.** Análise Exploratória de Dados
* O objetivo de uma análise exploratória de dados (EDA - do inglês: Exploratory Data Analysis) é entender como as variáveis impactam no fenômeno a ser modelado e encontrar insights que ajudem a solucionar o problema. 

**5.** Preparação dos Dados
* Aqui é feito a preparação dos dados para aplicar os modelos de aprendizado de máquina.

**6.** Seleção de Atributos
* Nesta etapa será selecionado as variáveis mais relevantes para o modelo. Aqui foi utilizado o Algoritmo Boruta.

**7.** Modelos de Aprendizagem de Máquina
* Seleciona-se alguns algoritmos de aprendizagem de máquina e realiza o treinamento e teste para observar qual modelo performa melhor.

**8.** Ajuste Fino de Hiperparâmetros
* Ajuste dos hiperparâmetros de forma que o modelo de aprendizado de máquina performe ainda melhor.

**9.** Interpretação de Erros e Conversão em Valores de Negócios
* A partir do melhor modelo encontrado nos passos 7 e 8, é feito a interpretação de alguns erros e como convertê-los de forma a entender qual será o retorno financeiro para a empresa em utilizar o modelo.

**10.** Deploy do Modelo em Produção
* Colocar o modelo em produção no Heroku de forma que qualquer um possa utilizar a partir da requisição na API. Também acessível pelo aplicativo do Telegram.

## 4. Top 5 Insights

**1.** Lojas com maior sortemento deveriam vender mais.
* Falsa. Lojas com maior sortimento vendem menos

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/insight1.png?raw=true)

É possível concluir que basic e extended tem aproximadamente o mesmo volume de vendas, mas o extra tem uma quantidade de venda menor. Considerou-se aqui que extra tem um volume maior, uma vez que não tenho tantas informações sobre o negócio.

**2.** Lojas com competidores mais próximos deveriam vender menos.
* Falsa. Lojas com competidores mais próximos vendem mais.

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/insight2.png?raw=true)

Pela lógica, se o competidor estiver mais próximo, a loja venderia menos. Porém, pelos dados, lojas com competidores mais próximos vendem MAIS. Isto é completamente contra qualquer senso comum.

**3.** Lojas com mais promoções consecutivas deveriam vender mais.
* Falsa Lojas com mais promoções consecutivas vendem menos.

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/insight3a.png?raw=true)

É possível observar que o menor valor é quando a loja participou só da promo2, as lojas que participaram das duas pomoções venderam semelhante a quando não tinha promoção alguma. As lojas que participaram apenas da promoção normal venderam mais.

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/insight3b.png?raw=true)

Pode-se observar que as vendas para a promoção tradicional + estendida foram menores.

**4.** Lojas abertas durante o feriado de Natal deveriam vender mais.
* Falsa Lojas abertas durante o feriado de Natal vendem menos.

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/insight4a.png?raw=true)

Vê-se que os feriados públicos tem muito mais vendas. O Natal é o feriado que vende menos e esse comportamento ocorre nos últimos anos da análise. Além disso, foi necessário remover os dias regulares pelo fato de serem muito mais dias, o que impossibilitaria uma análise precisa. No ano de 2015 não há natal, pois os dados vão até agosto de 2015.	

**5.** Lojas deveriam vender mais ao longo dos anos.
* Falsa Lojas vendem menos ao longo dos anos.

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/insight5.png?raw=true)
Podemos observar uma queda de venda entre os anos. A tendência é de decaimento, mesmo levando em conta que 2015 não está com os dados fechados, é possível observar uma queda de 2013 pra 2014.

## 5. Modelos de Machine Learning

Os modelos utilizados neste passo foram:

* Average Model (baseline para comparação)
* Linear Regression Model
* Linear Regression Regularized Model (Lasso)
* Random Forest Regressor
* XGBoost Regressor

Ou seja, uma média para servir de base de comparação, dois modelos lineares e dois não-lineares.

## 6. Performance dos modelos de machine learning

Como o problema tem uma ordem cronológica, é importante utilizar a técnica de Time Series Cross-Validation, de forma a ver a real performance de cada modelo e levar em conta a variável temporal do problema. A performance foi avaliada a partir do Erro Médio Absoluto (MAE), Erro Percentual Médio Absoluto (MAPE) e a Raiz Quadrada do Erro-Médio (RMSE). A performance real dos modelos é dada pela média dos erros +/- o desvio padrão do erro

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/modelos_cv.png?raw=true)

O primeiro ponto a ser observado é que estamos lidando com um problema não linear, uma vez que o melhor resultado foi encontrado usando o modelo de Random Forest. Mesmo a RF sendo o melhor modelo encontrado, aqui, será utilizado o modelo XGBoost. A princípio causa uma estranheza o modelo escolhido ser o que performou pior, porém, vale salientar que uma RF consome muito mais capacidade computacional que qualquer outro modelo, de forma que vale o risco de fazer os ajustes finos de uma XGBoost e observar como ela se comporta. É importante lembrar que está sendo utilizado o método CRIPS-DS, então, caso não seja encontrado um resultado satisfatório, em um próximo cíclo será utilizado o modelo de RF. 

## 7. Performance após ajuste fino dos hiperparâmetros (Hyperparameter Fine Tuning)
Após a aplicação do Algoritmo Boruta para definir os melhores hiperparâmetros o resultado foi o seguinte

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/xgboost_fine_tunned.png?raw=true)

É possível observar uma queda significativa dos erros aqui em comparação aos passos anteriores. 

## 8. Tradução do erro em métricas de negócio
A partir das análises feitas, define-se três cenários possíveis: o previsto, onde a loja terá um faturamento próximo ao do modelo, o melhor cenário, onde o faturamento será o valor previsto - MAE, enquanto o pior cenário é quando tem-se o faturamento com o maior erro possível, ou seja, faturamento + MAE.

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/scenarios.png?raw=true)

O gráfico abaixo mostra, para cada loja, o erro percentual e a predição. É possível ver que algumas lojas tem um erro bem grande, algo em torno de 50%. A maioria se encontra com um erro de até 10%. Munido destes resultados o CFO poderá definir qual a melhor estratégia para cada loja.

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/mapeXstore.png?raw=true)

### 8.1 Performance do Machine Learning

![alt text](https://github.com/CaioMendes92/RossmannStoreSales/blob/main/img/ML_performance.png?raw=true)

* Em (1,1), é possível ver que as predições das lojas estão bem próximas do resultado de teste ao longo do tempo, o que é um indicativo que o modelo performou bem.
* Em (1,2) é a porcentagem das previsões em relação a venda, a error_rate. Acima da linha 1, o modelo superestiou o resultado, abaixo ele subestimou.
* Em (2,1) vê-se que o erro tem uma distribuição bem próxima de uma normal, isso é importante pois é um indicativo que os erros estão bem próximos de 0.
* Em (2,2) é possível ver que previsões entre valores de 5k e 10k tem os maiores erros. Em termos da análise de resíduo, o modelo está como um "tubo" exceto por alguns outliers, o que a teoria dos resíduos indica como sendo o melhor resultado.

## 9. Deploy
As previsões podem ser acessadas via API ou pelo aplicativo Telegram

* URL para acessar a API: https://rossmann-model-caio.herokuapp.com/rossmann/predict
* Para acessar via telegram: https://t.me/rossmann_caio_bot

## 10. Conclusões
* A partir da taxa de erro podemos considerar que o resultado encontrado aqui é satisfatório, uma vez que o erro é de 11% para mais ou para menos, em algumas lojas sendo este erro ainda menor. 
* Verificou-se também que o modelo tende a subestimar o valor das previsões em 1,9%.

## 11. Lições Aprendidas

* Aprender modelos de aprendizado de máquina é importante, entretanto, entender a questão de negócio e saber converter os erros em resultados reais é tão importante quanto.
* Sempre existirá mais de uma forma de resolver um problema, com o conhecimento das técnicas é possível eliminar os piores, porém, para definir qual o melhor para o seu problema, é necessário testar.
* Aprendizado de máquina é apenas uma das funções de um cientista de dados, não a única.
