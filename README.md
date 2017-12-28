# *Latent Space Representation of Audio*

## WaveNet Autoencoder
WaveNet autoencoder merupakan sebuah *generative model* yang menggunakan raw audio waveform secara langsung sebagai input [1]. 
Selain itu, WaveNet autoencoder juga disebut sebagai *autoregressive model* dimana prediksi dari setiap sampel tidak hanya 
dipengaruhi oleh sebuah sampel sebelumnya, namun juga semua sampel sebelumnya. <br /><br />
WaveNet autoencoder memanfaatkan *dilated convolution layer* baik pada proses *encoder* maupun pada proses *decoder*. 
Penggunaan *convolution layers* ini membutuhkan waktu yang lebih cepat dibandingkan dengan penggunaan RNN yang biasanya 
digunakan sebagai model pada *sequencing data*. Hal ini disebabkan karena *convolution layers* tidak membutuhkan *recurrent 
connection* pada aplikasinya. Penjelasan lebih jauh mengenai WaveNet autoencoder dapat dilihat pada
[WaveNet autoencoder](https://magenta.tensorflow.org/nsynth).<br /><br />

## *Latent Space Representation*
*Latent space* yang dihasilkan oleh autoencoder dapat menjadi fitur representasi tingkat tinggi (*high level representation*) 
dari sebuah audio [2]. Pada penelitiannya, Sarrof & Casey, memanfaatkan autoencoder untuk mendapatkan representasi tingkat tinggi 
(*high level representation*) dari fitur audio yang dilatih dari *low level audio features* (seperti MFCC, *chroma feature*, dll).
<br /><br />
Pada dasarnya, WaveNet autoencoder digunakan sebagai *generative model* dalam mensintesis musik. 
Dalam hal ini, *latent space representation* z dari audio sangat mempengaruhi pembentukan musik baru dari data latih yang telah ada. 
Selain itu, *latent space* z ini dapat dimanfaatkan dalam berbagai bidang, seperti interpolasi dari dua audio. 
Engel dkk [1] menemukan bahwa, interpolasi dari dua audio menggunakan *latent space* z dari WaveNet autoencoder tidak hanya membuat 
terjadinya percampuran suara dari 2 audio berbeda, namun juga dapat membentuk terjadinya percampuran dinamika seiring berjalannya 
waktu dari audio tersebut. 
Artinya, WaveNet autoencoder dapat menyimpan aspek timber dan dinamika dari sebuah audio.<br /><br />
*Latent Space Representation* dari autoencoder dapat dimanfaatkan dalam proses pengenalan emosi pada musik.
Hasil eksperimen penulis menunjukkan bahwa *latent space* tersebut memberikan performa yang cukup baik dalam pengenalan emosi
menggunakan model *valence-arousal* (V-A) [3] pada komponen arousal dari musik. 

## References
[1] J. Engel, C. Resnick, A. Roberts, S. Dieleman, M. Norouzi, D. Eck and K. Simonyan, "Neural Audio Synthesis of Musical Notes with WaveNet Autoencoders," in Proceeding of the 34th International Conference on Machine Learning, Sidney, Australia, 2017.
<br />
[2] A. M. Sarrof and M. Casey, "Musical Audio Synthesis Using Autoencoding Neural Nets," in Proceedings - 40th International Computer Music Conference, ICMC 2014 and 11th Sound and Music Computing Conference, SMC 2014, US, 2014.
<br />
[3] J. A. Russell, "A Circumplex Model of Affect," Journal of Personality and Social Psychology, vol. 39, no. 6, pp. 1161-1178, December 1980.
