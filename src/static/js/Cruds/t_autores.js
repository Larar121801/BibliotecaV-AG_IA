function obtenerAutores() {
    fetch('/autores')
      .then(response => response.json())
      .then(data => {
        const tabla = document.getElementById('tabla-autores');
        const tbody = tabla.getElementsByTagName('tbody')[0];
        tbody.innerHTML = '';
        data.autor.forEach(fila => {
          const tr = document.createElement('tr');
          const tdId = document.createElement('td');
          tdId.innerText = fila.id;
          const tdNombre = document.createElement('td');
          tdNombre.innerText = fila.nombre;
          const tdNacionalidad = document.createElement('td');
          tdNacionalidad.innerText = fila.nacionalidad;
          const tdBiografia = document.createElement('td');
          tdBiografia.innerText = fila.biografia;
          tr.appendChild(tdId);
          tr.appendChild(tdNombre);
          tr.appendChild(tdNacionalidad);
          tr.appendChild(tdBiografia);
          tbody.appendChild(tr);
        });
      });
  }

  const formAgregarAutor = document.getElementById('form-agregar-autor');
  formAgregarAutor.addEventListener('submit', (event) => {
    event.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const nacionalidad = document.getElementById('nacionalidad').value;
    const biografia = document.getElementById('biografia').value;
    const data = { nombre, nacionalidad, biografia };
    fetch('/autores', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      obtenerAutores();
      alert(data.mensaje);
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Ocurrió un error al agregar el autor');
    });
  });
