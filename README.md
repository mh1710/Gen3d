# GEN3D

Meu nome é [Matheus](https://www.linkedin.com/in/dev-matheus-henrique) e venho aqui apresentar meu ultimo projeto. O Gen3d consiste em 3 ferramentas que em um futuro próximo serão unidas para melhorar a experiencia do usuário, se quiser unir fique a vontade ou se quiser fazer uma parceria para codarmos junto, entre em contato com meu email e linkedin na página inicial.

Os projetos estão hospedados em spaces no Hugging Face, pois lá estamos utilizando a placa de vídeo Nvidia A100 de forma gratuita através de Gradio APP, entre nos links abaixo e testem. Fique a vontade também para alterar o codigo da maneira que achar mais útil.

O Gen3d acontece em 3 etapas:

1° [Aidiffusion](https://huggingface.co/spaces/Mathdesenvnonimate/aidiffusion) - Aqui geramos as imagens que iremos transformar em modelos 3d, no caso abaixo ela foi otimizada com Lora para gerar bonecos FunkoPOP, para modificar LORA é só alterar o código com o modelo que voce queira e que também esteja hospedado no hugging face. Essa etapa é opcional, pois caso voce já tenha a imagem que voce queira transformar, pule para a etapa 2.

2° [LGM](https://huggingface.co/spaces/Mathdesenvnonimate/LGM) - Aqui a imagem que voce já tenha, ou tenha gerado, voce sobe e irá gerar um video 3D para visualização prévia, caso fique ruim voce tem a possibilidade de fazer um ajuste fino a partir da adição de um prompt, prompt negativo, barra de elevação, passos de inferencia e seeds aleatoria.

3° [TSR](https://huggingface.co/spaces/Mathdesenvnonimate/TripoSR) - Aqui utilizamos o modelo TripoSR para gerar o nosso modelo 3d, depois de muitos testes percebi que o TripoSR é o melhor modelo de geração 3D sem usar excessivo poder computacional (A explicação disso e dos modelos testados podem vir a ser uma publicação no Linkedin ou no Médium).\
Com a mesma imagem gerada no primeiro passo voce sobe e gera um modelo 3d nos formatos OBJ e STL, mas as saidas podem também ser adaptadas no código.\
Os ajustes finos ficam a partir da mudança da remoção do background (se sua imagem tiver fundo transparente desative essa opção), da proporção de primeiro plano e da resolução Marching Cubes, caso voce não saiba o que é, segue um artigo em pdf da PUC com a explicação (https://www.maxwell.vrac.puc-rio.br/15358/15358_5.PDF).

Todo o processo demora em torno de 2 minutos á 5 minutos, para modeladores 3D, designers e outros tipos de usuários que trabalham com projetos 3ds, essa ferramenta podem auxiliar muito no processo sendo somente ajustar detalhes pois a ferramenta gera resultados com qualidade mas ainda não são todos os modelos que serão gerados com excelencia. 

Caso queira discutir sobre o projeto ou queira propor melhorias ou contratar meus serviços, me contate a partir das minhas redes sociais que estão na minha página inicial do github, ou pelo meu [Linkedin](https://www.linkedin.com/in/dev-matheus-henrique/).
