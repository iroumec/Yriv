% Defino una lista de temáticas.
topics(['Mandela', 'Schrodinger', 'Mariposa']).

% Predicado para elegir una temática aleatoria.
random_tematica(X) :-
    topics(TopicList),
    random_member(X, TopicList).

enlace('Mandela', 'https://www.youtube.com/watch?v=J7J4Rr8cWJE').
enlace('Schrodinger', 'https://www.youtube.com/watch?v=j5vCOVXliuc').
enlace('Mariposa', 'https://www.youtube.com/watch?v=J7J4Rr8cWJE').

descripcion('Mandela', '¿Cómo es la cola de Pikachu? ¿La marca de chocolates KitKat lleva guion? ¿Estás seguro de tus respuestas? ¡Espero que este video en la lista de mis favoritos te vuele la cabeza tanto como a mí! :D').
descripcion('Schrodinger', '¿Alguna vez te preguntaste cómo algo puede estar vivo y muerto a la vez? Entonces te va a encantar este video en mi lista de favoritos :)').
descripcion('Mariposa', 'Se dice que el aleteo de una mariposa en Brasil puede generar un huracán en Estados Unidos... Si estás tan sorprendido como yo de tal afirmación, este video en mi lista de favoritos te fascinará. :)').