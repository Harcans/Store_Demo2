async function loadProducts() {
  const res = await fetch("/api/products");
  const products = await res.json();
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  products.forEach(p => grid.appendChild(makeCard(p)));
}

function makeCard(p) {
  const card = document.createElement("div");
  card.className = "card";
  let badge;
  if (p.stock === 0) badge = '<span class="badge out">Out of stock</span>';
  else if (p.stock < 6) badge = `<span class="badge low">Low stock — ${p.stock} left!</span>`;
  else badge = `<span class="badge in">In stock: ${p.stock}</span>`;
  card.innerHTML = `
    <div class="emoji">${p.emoji}</div>
    <h3>${p.name}</h3>
    <div class="price">$${p.price.toFixed(2)}</div>
    ${badge}<br>
    <button class="buy" ${p.stock === 0 ? "disabled" : ""} onclick="buy(${p.id}, this)">Buy 1</button>
    <div class="msg"></div>`;
  return card;
}

async function buy(id, btn) {
  const res = await fetch("/api/buy", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, qty: 1 })
  });
  const data = await res.json();
  if (!res.ok) {
    btn.parentElement.querySelector(".msg").textContent = data.error;
    return;
  }
  await loadProducts();
}

loadProducts();
