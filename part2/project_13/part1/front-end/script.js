// script.js

const url = 'http://localhost:8000/api/contacts/'

window.getContacts = async function (skip = 0, limit = 100) {
  const response = await fetch(`${url}?skip=${skip}&limit=${limit}`)
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  const contacts = await response.json()
  return contacts
}

window.createContact = async function (contact) {
  const response = await fetch(`${url}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(contact),
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}

window.editContact = async function (contact) {
  const response = await fetch(`${url}${contact.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(contact),
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}

window.deleteContact = async function (id) {
  const response = await fetch(`${url}${id}`, {
    method: 'DELETE',
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}

window.getBirthdays = async function (contacts) {
  try {
    const response = await fetch('http://localhost:8000/api/contacts/birthdays/');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const birthdays = await response.json();
    contacts.splice(0, contacts.length, ...birthdays); // Оновити стан contacts
  } catch (error) {
    console.error('Error fetching birthdays:', error.message || error);
  }
}

async function searchContacts() {
  const firstName = document.getElementById('first_name').value.trim();
  const lastName = document.getElementById('last_name').value.trim();
  const email = document.getElementById('email').value.trim();

  const query = [];
  if (firstName) query.push(`first_name=${firstName}`);
  if (lastName) query.push(`last_name=${lastName}`);
  if (email) query.push(`email=${email}`);

  const queryString = query.join('&');
  const searchUrl = `${url}search?${queryString}`;

  try {
    const response = await fetch(searchUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const contacts = await response.json();
    displaySearchResults(contacts);
  } catch (error) {
    console.error('Error searching contacts:', error.message || error);
  }
}

function displaySearchResults(contacts) {
  const searchResults = document.getElementById('searchResults');
  searchResults.innerHTML = '';

  if (contacts.length === 0) {
    searchResults.innerHTML = '<p>No contacts found.</p>';
    return;
  }

  const table = document.createElement('table');
  table.className = 'table table-striped';
  const thead = document.createElement('thead');
  thead.innerHTML = `
    <tr>
      <th scope="col">ID</th>
      <th scope="col">First Name</th>
      <th scope="col">Last Name</th>
      <th scope="col">Email</th>
      <th scope="col">Phone Number</th>
      <th scope="col">Birthday</th>
      <th scope="col">Description</th>
    </tr>
  `;
  const tbody = document.createElement('tbody');
  contacts.forEach(contact => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${contact.id}</td>
      <td>${contact.first_name}</td>
      <td>${contact.last_name}</td>
      <td>${contact.email}</td>
      <td>${contact.phone_number}</td>
      <td>${contact.birthday}</td>
      <td>${contact.description}</td>
    `;
    tbody.appendChild(row);
  });
  table.appendChild(thead);
  table.appendChild(tbody);
  searchResults.appendChild(table);
}

