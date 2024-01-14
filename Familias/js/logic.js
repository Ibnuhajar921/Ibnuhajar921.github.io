// Membuat objek XMLHttpRequest
var xhr = new XMLHttpRequest();

// Mengatur callback untuk menangani respon dari server
xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
            // Jika permintaan sukses (status kode 200)
            var response = xhr.responseText;
            // Lakukan sesuatu dengan response dari server
            console.log(response);
        } else {
            // Menangani kesalahan jika permintaan tidak berhasil
            console.error('Terjadi kesalahan: ' + xhr.status);
        }
    }
};

// Membuat permintaan GET ke server
xhr.open('GET', 'https://contoh.com/api/products', true);
xhr.send();
