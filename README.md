
# Tech Blog

Este projeto pessoal é uma aplicação fullstack com as principais funcionalidades de um blog.

Foi desenvolvido com o proposito de aperfeiçoar meus conhecimentos nas seguites tecnologias:

 - Python;
 - Django;
 - Django-rest-framework;
 - Postgre SQL;
 - Testes Unitários;
 - Modelo Arquitetural Rest;
 - HTML, CSS, JavaScript e Bootstrap.

 O sistema foi hospedado no heroku e pode ser acessado através do [link](https://restful-tech-blog.herokuapp.com/).
***
 # Desafios

 O sistema consta com autenticação via Token e login social com o gmail, o que foi o maior desafio do projeto, visto que é necessário entender um pouco mais sobre o que é o oAuth2 e utilizar serviços de terceiros, no caso google.
 ***
 # Créditos
  O front-end da aplicação foi personalizado a partir de um template que pode ser encontraado [aqui](https://startbootstrap.com/theme/clean-blog)
***


 



## Referência da API

#### Busca por todos os posts do blog

```http
  GET /api/posts
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `format` | `string` | **Obrigatório**. Formato da response. Opções: json e api |
| `limit` | `integer` | **Opcional**. Quantidade de items para limitar a response |

#### Busca por comentários para uma dado post

```http
  GET /api/comments?post_id=${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `uuid` | **Obrigatório**. Id do post para a busca de comentários |

