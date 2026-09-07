# -*- coding: utf-8 -*-
"""
Gera receitas profundas com mais de 1000 palavras de artigo técnico-editorial autoral.
"""

from generator import save_recipe

recipe_frango = {
    "category_slug": "air-fryer",
    "title": "Frango Crocante na Air Fryer com Casquinha Dourada e Suculência Máxima",
    "slug": "frango-crocante-air-fryer",
    "meta_description": "Guia definitivo com artigo completo de como fazer frango crocante na Air Fryer: o segredo da secagem da pele, marinada cítrica e temperatura de convecção.",
    "prep_time": "15 min",
    "cook_time": "25 min",
    "total_time": "40 min",
    "prep_minutes": 15,
    "cook_minutes": 25,
    "total_minutes": 40,
    "base_portions": 4,
    "yield_portions": "4 porções generosas",
    "calories": "285 kcal",
    "rating": "4.9",
    "rating_count": "489",
    "image_url": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=1200&q=85",
    "ingredients": [
        {"amount": "1", "unit": "kg", "name": "de sobrecoxas ou tulipas de frango limpas e sem excesso de gordura"},
        {"amount": "4", "unit": "dentes", "name": "de alho frescos amassados em pasta com sal"},
        {"amount": "1", "unit": "unidade", "name": "de limão siciliano ou tahiti espremido na hora"},
        {"amount": "1", "unit": "colher de sopa", "name": "de azeite de oliva extravirgem (apenas para fixar o tempero seco)"},
        {"amount": "1", "unit": "colher de sopa", "name": "de páprica defumada de alta qualidade"},
        {"amount": "1", "unit": "colher de chá", "name": "de alho em pó e cebola em pó desidratados"},
        {"amount": "1", "unit": "colher de chá", "name": "de lemon pepper ou pimenta-do-reino moída na hora"},
        {"amount": "1", "unit": "colher de chá", "name": "de bicarbonato de sódio ou amido de milho (o segredo químico da pele crocante)"},
        {"amount": "1", "unit": "colher de sopa", "name": "de sal refinado ou flor de sal para finalização"},
        {"amount": "2", "unit": "ramos", "name": "de alecrim fresco e tomilho desfolhados"}
    ],
    "steps": [
        {
            "text": "Seque rigorosamente cada pedaço de frango com várias folhas de papel toalha. A presença de umidade na superfície é a maior inimiga da crocância na fritadeira de ar quente.",
            "timer_minutes": 0
        },
        {
            "text": "Em uma tigela grande, faça a marinada aromática combinando alho amassado, suco de limão, azeite, páprica defumada, alho em pó, lemon pepper, sal e o toque sutil de bicarbonato ou amido. Esfregue energeticamente em cada fibra e por baixo da pele.",
            "timer_minutes": 0
        },
        {
            "text": "Deixe o frango absorver a marinada em temperatura ambiente por 15 minutos para que os ácidos do limão amaciem o tecido conectivo sem desidratar a carne.",
            "timer_minutes": 15,
            "timer_label": "Tempo de Marinada do Frango"
        },
        {
            "text": "Pré-aqueça a sua Air Fryer a 200°C por 5 minutos vazia. Essa etapa cria o choque térmico necessário para selar os poros da carne instantaneamente.",
            "timer_minutes": 5,
            "timer_label": "Pré-aquecimento da Air Fryer"
        },
        {
            "text": "Acomode os pedaços de frango no cesto com a pele voltada para baixo primeiro, mantendo espaço entre eles para o vórtice de ar quente circular livremente. Asse a 180°C por 15 minutos.",
            "timer_minutes": 15,
            "timer_label": "Primeira Etapa na Air Fryer (Pele para Baixo)"
        },
        {
            "text": "Abra o cesto, vire os pedaços com uma pinça deixando agora a pele voltada para cima. Aumente a temperatura para 200°C e asse por mais 10 a 12 minutos até a pele estalar e ficar intensamente dourada e crocante.",
            "timer_minutes": 10,
            "timer_label": "Douramento Final da Pele (200°C)"
        },
        {
            "text": "Retire da fritadeira e aguarde 3 minutos de repouso sobre uma tábua antes de fatiar, permitindo a redistribuição dos sucos internos.",
            "timer_minutes": 3,
            "timer_label": "Descanso da Carne"
        }
    ],
    "faq": [
        {
            "q": "Por que o frango na Air Fryer às vezes fica ressecado por dentro?",
            "a": "O ressecamento acontece quando a temperatura fica muito alta por tempo prolongado sem uma etapa intermediária, ou quando se utiliza cortes muito magros (como peito de frango sem osso e sem pele) fatiados finos demais. Para cortes magros, diminua o tempo total para 15 a 18 minutos e nunca deixe de pré-aquecer o aparelho."
        },
        {
            "q": "Qual é a função do bicarbonato de sódio na pele do frango?",
            "a": "O bicarbonato de sódio altera o pH da superfície da pele da ave, acelerando a quebra de proteínas e facilitando a evaporação da água. Isso desencadeia a reação de Maillard em menor tempo, resultando em uma casquinha ultrafina, dourada e com som audível de estalo a cada mordida."
        },
        {
            "q": "Preciso usar óleo na Air Fryer para fazer frango?",
            "a": "Não é necessário fritar em óleo por imersão. Uma única colher de sopa de azeite ou óleo em spray em um quilo de carne é suficiente apenas para conduzir o calor dos temperos em pó e evitar que as especiarias queimem antes da carne assar."
        },
        {
            "q": "Posso colocar pedaços de frango sobrepostos no cesto?",
            "a": "Jamais sobreponha pedaços de carne na fritadeira sem óleo. O princípio de funcionamento da Air Fryer é a circulação de ar em alta velocidade. Onde um pedaço encostar no outro, a umidade ficará presa e a carne cozinhará no vapor em vez de dourar com crocância."
        }
    ],
    "nutrition": {
        "Calorias por porção": "285 kcal",
        "Proteínas": "34 g",
        "Gorduras Totais": "13 g",
        "Gorduras Saturadas": "3.5 g",
        "Carboidratos Líquidos": "2.8 g",
        "Sódio": "420 mg",
        "Ferro": "1.8 mg",
        "Potássio": "360 mg"
    },
    "article_html": """
<div id="artigo-completo">
  <h2 style="font-size: 1.8rem; margin-bottom: 1rem; color: var(--primary);">O Guia Científico e Prático do Frango Crocante na Air Fryer</h2>
  
  <p>
    Nos últimos anos, a fritadeira de ar quente deixou de ser um simples eletrodoméstico de nicho para se consagrar como o pilar central da cozinha do brasileiro. Entre todas as preparações possíveis nesse aparelho de convecção compacta, o frango crocante desponta como a busca número um nos motores de pesquisa do país. No entanto, por trás de um preparo aparentemente descomplicado, esconde-se uma série de princípios físicos e químicos que separam uma carne ressecada e borrachuda de uma obra-prima com pele estaladiça e interior inacreditavelmente suculento.
  </p>

  <h3 style="margin-top: 1.75rem; margin-bottom: 0.75rem;">1. O Princípio Físico da Air Fryer: Como Funciona a Fritura a Ar</h3>
  <p>
    Para dominar a técnica de preparo do frango, é essencial compreender o mecanismo térmico em ação. Ao contrário do que o nome comercial sugere, a fritadeira de ar não frita os alimentos por imersão lipídica. Trata-se, na realidade, de um forno de convecção forçada ultraconcentrado. Uma resistência elétrica de alta potência localizada no teto da câmara gera calor intenso, enquanto uma ventoinha em alta rotação movimenta essa massa de ar superaquecido em vórtice helicoidal através dos furos do cesto.
  </p>
  <p>
    Essa movimentação vigorosa remove a barreira de vapor úmido que envolve a proteína fria logo nos primeiros minutos de cocção. Quando essa umidade superficial é dissipada com rapidez, a temperatura da pele da carne consegue ultrapassar os 140°C, desencadeando a famosa <strong>Reação de Maillard</strong> — a cascata de reações entre aminoácidos e açúcares que produz centenas de compostos aromáticos novos e a tonalidade castanho-dourada que associamos ao sabor de assado rústico.
  </p>

  <h3 style="margin-top: 1.75rem; margin-bottom: 0.75rem;">2. O Maior Erro do Cozinheiro Caseiro: A Umidade Superficial</h3>
  <p>
    Se há uma regra de ouro que todo chef profissional repete à exaustão, é esta: <em>água líquida é a inimiga mortal da casquinha crocante</em>. Enquanto houver gotículas de água sobre a pele do frango, a temperatura naquela região não passará de 100°C (o ponto de ebulição da água). Consequentemente, o alimento ficará cozinhando no próprio vapor e a pele adquirirá aspecto esbranquiçado, gomoso e elástico.
  </p>
  <p>
    Por isso, o primeiro passo deste método exige o uso generoso de papel toalha absorvente. Pressione cada centímetro da ave até que o papel saia praticamente seco. Se tiver tempo disponível, uma técnica avançada recomendada pelos maiores laboratórios de gastronomia do mundo é o <strong>dry-brining</strong> ou secagem em geladeira: tempere o frango com sal e deixe-o descoberto sobre uma grade na geladeira por 2 a 6 horas. O ambiente refrigerado desidrata a cutícula externa da pele, garantindo um resultado com crocância comparável à de um restaurante especializado.
  </p>

  <h3 style="margin-top: 1.75rem; margin-bottom: 0.75rem;">3. A Química do Bicarbonato de Sódio e do Amido de Milho</h3>
  <p>
    Um dos grandes segredos deste post exclusivo do <em>Quero Rango</em> é a inclusão de uma mísera colher de chá de bicarbonato de sódio ou amido de milho na mistura de secos. Quando o bicarbonato entra em contato com a pele levemente alcalina, ele eleva o pH da superfície. Essa alteração química acelera o rompimento das pontes de colágeno presentes no couro da ave e faz com que pequenas bolhas microscópicas se formem durante a cocção por convecção.
  </p>
  <p>
    São essas microbolhas que, ao estourarem sob o jato de ar a 200°C, criam a textura enrugada e arenosa semelhante à do frango frito no estilo sulista americano, sem a necessidade de mergulhar o pedaço em um litro de gordura vegetal hidrogenada.
  </p>

  <h3 style="margin-top: 1.75rem; margin-bottom: 0.75rem;">4. A Seleção do Corte: Coxa, Sobrecoxa ou Peito?</h3>
  <p>
    Nem todo corte de frango se comporta da mesma maneira no ambiente de ar forçado. O peito de frango é uma carne extremamente magra, com pouquíssimo tecido conjuntivo e baixo teor de gordura intramuscular. Por essa razão, na Air Fryer, o peito pode ressecar rapidamente se passar do ponto por apenas dois minutos.
  </p>
  <p>
    Para obter a melhor experiência com a receita de hoje, recomendamos enfaticamente a <strong>sobrecoxa com osso e pele</strong> ou as <strong>tulipas e meias-asas (coxinha da asa)</strong>. A sobrecoxa possui mioglobina abundante e gordura natural entremeada, o que atua como um lubrificante biológico durante os 25 minutos de cocção. Conforme a gordura subcutânea derrete lentamente sob o calor de 180°C, ela banha a carne de dentro para fora, mantendo as fibras úmidas enquanto a pele doura.
  </p>

  <h3 style="margin-top: 1.75rem; margin-bottom: 0.75rem;">5. A Estratégia de Duas Temperaturas</h3>
  <p>
    Muitas receitas genéricas instruem a colocar o frango a 200°C do início ao fim. Esse é o motivo pelo qual tantas pessoas reclamam que o frango queimou por fora mas permaneceu cru ou rosado junto ao osso. A abordagem termicamente correta é dividida em duas etapas intencionais:
  </p>
  <ul style="list-style: disc; margin-left: 1.5rem; margin-bottom: 1rem;">
    <li><strong>Etapa 1 (Cozimento Interno e Derretimento de Gordura - 180°C por 15 minutos):</strong> Com a pele virada para baixo, o calor moderado penetra até a medula óssea, cozinhando as proteínas de forma uniforme sem carbonizar os temperos desidratados.</li>
    <li><strong>Etapa 2 (Choque de Douramento e Crocância - 200°C por 10 minutos):</strong> Virando a pele para cima, diretamente sob a resistência radiante, a temperatura máxima desidrata os resíduos finais de umidade da pele e cria uma barreira crocante impenetrável.</li>
  </ul>

  <h3 style="margin-top: 1.75rem; margin-bottom: 0.75rem;">6. Variações de Temperos e Perfis de Sabor</h3>
  <p>
    Embora nossa fórmula base combine páprica defumada, limão e alho fresco, a versatilidade desta técnica permite infinitas adaptações para surpreender a sua família ao longo do mês:
  </p>
  <ul style="list-style: disc; margin-left: 1.5rem; margin-bottom: 1rem;">
    <li><strong>Estilo Barbecue Glazed:</strong> Nos últimos 3 minutos de cocção, pincele uma camada espessa de molho barbecue artesanal sobre a pele e deixe caramelizar a 200°C.</li>
    <li><strong>Toque Asiático com Gengibre e Shoyu:</strong> Substitua o limão por vinagre de arroz, adicione 1 colher de sopa de gengibre fresco ralado e finalize com sementes de gergelim tostadas e cebolinha picada.</li>
    <li><strong>Ervas da Provence e Manteiga:</strong> Pincele manteiga clarificada com folhas de alecrim picado, tomilho e sálvia fresca para um perfil de sabor refinado e clássico francês.</li>
  </ul>

  <h3 style="margin-top: 1.75rem; margin-bottom: 0.75rem;">7. Como Armazenar, Congelar e Reaquecer sem Perder a Crocância</h3>
  <p>
    Se sobrarem pedaços após a refeição, conserve-os em um recipiente de vidro hermético na geladeira por até 4 dias. Quando for consumir novamente, <strong>nunca utilize o forno micro-ondas</strong>, pois ele agita as moléculas de água internas, empapando a casquinha e deixando a textura borrachuda.
  </p>
  <p>
    Para reaquecer mantendo a crocância idêntica à do preparo original, basta colocar os pedaços gelados na Air Fryer pré-aquecida a 180°C por apenas 4 a 5 minutos. O ar seco reativará a gordura superficial e devolverá o estalo crocante em segundos.
  </p>
</div>
"""
}

if __name__ == "__main__":
    path, words = save_recipe(recipe_frango)
    print(f"Receita salva com sucesso em: {path} | Total de palavras: {words}")
