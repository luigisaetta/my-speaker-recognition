## The frontend

The Frontend / UI has been developed using Open Source technology as **Angular, 
Bootstrap and jQuery**. 

To maximize the result and minimize the time spent to 
develop, we didn’t begin from scratch, but we used a template (the mention is on 
the footer). 

Nowadays, we have many technologies and reusable frameworks that enable us to 
reach great result without spend time on “low level programming”, and with this 
project we tried to take advantage of that as much as possible.

The idea behind it has been to spend more time on developing the ML algorithm, 
because the quality of the product it is always important, nevertheless the 
presentation layer influence the first impression of the user on the product, than we
decide that it has to been somehow captivating.

To capture the audio from the browser we used the **Media Capture and Streams API** 
and **WebRTC**, in details the **MediaRecorder API**, that as is shown from the below 
image it is supported by most of the browser.

Strictly related to the fronted we can find the first microservice, a **NodeJS express** 
application that serve the website and expose different endpoints. 
This microservice allow the Browser to send the audio file recorded and then it 
perform the encoding thanks to the **FFmpeg** open-source libraries. Once encoded in 
