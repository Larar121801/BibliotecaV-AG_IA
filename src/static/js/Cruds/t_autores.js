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