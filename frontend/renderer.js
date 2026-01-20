(() => {
  const API = 'http://127.0.0.1:8000'

  // Views
  const loginView = document.getElementById('login-view')
  const clientsView = document.getElementById('clients-view')
  const loansView = document.getElementById('loans-view')

  const btnDashboard = document.getElementById('btn-dashboard')
  const btnClients = document.getElementById('btn-clients')
  const btnLoans = document.getElementById('btn-loans')

  const clientSearch = document.getElementById('client-search')
  const loanSearch = document.getElementById('loan-search')

  const modalRoot = document.getElementById('modal-root')
  const toasts = document.getElementById('toasts')

  const show = (v) => { loginView.classList.add('hidden'); clientsView.classList.add('hidden'); loansView.classList.add('hidden'); v.classList.remove('hidden') }

  btnClients.addEventListener('click', async () => { show(clientsView); await loadClients() })
  btnLoans.addEventListener('click', async () => { show(loansView); await loadLoans() })
  btnDashboard.addEventListener('click', () => { show(loginView) })

  // Toast helper
  function toast(message, type='info'){
    const el = document.createElement('div')
    el.className = `px-4 py-2 rounded shadow ${type==='error'?'bg-red-500 text-white':type==='success'?'bg-green-500 text-white':'bg-gray-800 text-white'}`
    el.textContent = message
    toasts.appendChild(el)
    setTimeout(()=> el.remove(), 4000)
  }

  // Global spinner
  const globalSpinner = document.getElementById('global-spinner')
  function setGlobalLoading(state){
    if(!globalSpinner) return
    if(state) globalSpinner.classList.remove('hidden')
    else globalSpinner.classList.add('hidden')
  }

  // Accessible focus management
  function trapFocus(modal){
    const focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
    if(focusable.length) focusable[0].focus()
  }

  // Login
  document.getElementById('btn-login').addEventListener('click', async () => {
    const u = document.getElementById('input-username').value.trim()
    const p = document.getElementById('input-password').value
    if(!u || !p){ toast('Preencha usuário e senha', 'error'); return }
    try {
      const res = await fetch(API + '/login', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username:u,password:p})})
      if (res.ok) {
        toast('Login bem sucedido', 'success')
        show(clientsView)
        await loadClients()
      } else {
        const j = await res.json()
        toast('Erro: ' + (j.detail || 'autenticação'), 'error')
      }
    } catch (e) { toast('Erro de conexão ao backend', 'error') }
  })

  // Create client modal
  document.getElementById('btn-new-client').addEventListener('click', () => {
    const modal = document.createElement('div')
    modal.className = 'fixed inset-0 bg-black/40 flex items-center justify-center z-50'
    modal.innerHTML = `
      <div role="dialog" aria-modal="true" class="bg-white rounded p-6 w-full max-w-lg">
        <h3 class="text-lg font-semibold mb-3">Novo Cliente</h3>
        <form id="form-client" onsubmit="return false;" class="space-y-3">
          <div><label class="block text-sm">Nome<input id="c_nome" class="w-full border rounded px-3 py-2"></label></div>
          <div class="grid grid-cols-2 gap-3"><label class="block text-sm">CPF/CNPJ<input id="c_cpf" class="w-full border rounded px-3 py-2"></label><label class="block text-sm">Telefone<input id="c_tel" class="w-full border rounded px-3 py-2"></label></div>
          <div><label class="block text-sm">Email<input id="c_email" class="w-full border rounded px-3 py-2"></label></div>
          <div class="flex justify-end gap-3 mt-4"><button id="cancel-client" class="px-4 py-2 bg-gray-200 rounded">Cancelar</button><button id="save-client" class="px-4 py-2 bg-blue-600 text-white rounded">Salvar</button></div>
        </form>
      </div>`
    modalRoot.appendChild(modal)
    trapFocus(modal)

    modal.querySelector('#cancel-client').addEventListener('click', ()=> modal.remove())
    modal.querySelector('#save-client').addEventListener('click', async ()=>{
      const nome = modal.querySelector('#c_nome').value.trim()
      const cpf = modal.querySelector('#c_cpf').value.trim()
      const tel = modal.querySelector('#c_tel').value.trim()
      const email = modal.querySelector('#c_email').value.trim()
      // Basic validation
      const emailRe = /^\S+@\S+\.\S+$/
      if(!nome || !cpf || !tel || !email){ toast('Preencha todos os campos', 'error'); return }
      if(!emailRe.test(email)){ toast('Email inválido', 'error'); return }
      setGlobalLoading(true)
      try{
        const res = await fetch(API + '/clients', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({nome, cpf_cnpj:cpf, telefone:tel, email, endereco:''})})
        if(res.ok){ toast('Cliente criado', 'success'); modal.remove(); await loadClients() }
        else{ const j = await res.json(); toast('Erro: ' + (j.detail||'falha'), 'error') }
      }catch(e){ toast('Erro criação cliente', 'error') }
      finally{ setGlobalLoading(false) }
    })
  })

  // Create loan modal with preview
  document.getElementById('btn-new-loan').addEventListener('click', async () => {
    // load clients for selection
    const clients = await (await fetch(API + '/clients')).json()
    const modal = document.createElement('div')
    modal.className = 'fixed inset-0 bg-black/40 flex items-center justify-center z-50 overflow-auto'
    modal.innerHTML = `
      <div role="dialog" aria-modal="true" class="bg-white rounded p-6 w-full max-w-2xl">
        <h3 class="text-lg font-semibold mb-3">Novo Empréstimo</h3>
        <form id="form-loan" onsubmit="return false;" class="space-y-3">
          <div><label class="block text-sm">Cliente<select id="l_cliente" class="w-full border rounded px-3 py-2">${clients.map(c=>`<option value="${c.id}">${c.nome} - ${c.cpf_cnpj}</option>`).join('')}</select></label></div>
          <div class="grid grid-cols-3 gap-3"><label class="block text-sm">Valor<input id="l_valor" type="number" step="0.01" class="w-full border rounded px-3 py-2"></label><label class="block text-sm">Taxa (%/mês)<input id="l_taxa" type="number" step="0.01" class="w-full border rounded px-3 py-2"></label><label class="block text-sm">Prazo (meses)<input id="l_prazo" type="number" class="w-full border rounded px-3 py-2"></label></div>
          <div id="loan-preview" class="p-3 bg-gray-50 rounded text-sm text-gray-700">Preencha os valores para ver o preview.</div>
          <div class="flex justify-end gap-3 mt-4"><button id="cancel-loan" class="px-4 py-2 bg-gray-200 rounded">Cancelar</button><button id="save-loan" class="px-4 py-2 bg-blue-600 text-white rounded">Criar Empréstimo</button></div>
        </form>
      </div>`
    modalRoot.appendChild(modal)
    trapFocus(modal)

    const valor = modal.querySelector('#l_valor')
    const taxa = modal.querySelector('#l_taxa')
    const prazo = modal.querySelector('#l_prazo')
    const preview = modal.querySelector('#loan-preview')

    function updatePreview(){
      const v = parseFloat(valor.value) || 0
      const t = parseFloat(taxa.value) || 0
      const p = parseInt(prazo.value) || 0
      if(v>0 && t>=0 && p>0){
        // juros compostos: total = v * (1 + t/100)^p
        const total = v * Math.pow(1 + (t/100), p)
        const parcela = total / p
        const juros = total - v
        preview.innerHTML = `<strong>Valor Total:</strong> R$ ${total.toFixed(2)} • <strong>Parcela:</strong> R$ ${parcela.toFixed(2)} • <strong>Juros:</strong> R$ ${juros.toFixed(2)}`
      } else preview.textContent = 'Preencha os valores para ver o preview.'
    }

    valor.addEventListener('input', updatePreview)
    taxa.addEventListener('input', updatePreview)
    prazo.addEventListener('input', updatePreview)

    modal.querySelector('#cancel-loan').addEventListener('click', ()=> modal.remove())
    modal.querySelector('#save-loan').addEventListener('click', async ()=>{
      const cliente_id = modal.querySelector('#l_cliente').value
      const valor_v = parseFloat(valor.value)
      const taxa_v = parseFloat(taxa.value)
      const prazo_v = parseInt(prazo.value)
      if(!cliente_id || !(valor_v>0) || !(taxa_v>=0) || !(prazo_v>0)){ toast('Preencha corretamente os valores (valor > 0, prazo > 0)', 'error'); return }
      setGlobalLoading(true)
      try{
        const res = await fetch(API + '/loans', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({cliente_id, valor_emprestado:valor_v, taxa_juros:taxa_v, data_emprestimo:new Date().toISOString(), prazo_meses:prazo_v})})
        if(res.ok){ toast('Empréstimo criado', 'success'); modal.remove(); await loadLoans() }
        else{ const j = await res.json(); toast('Erro: ' + (j.detail||'falha'), 'error') }
      }catch(e){ toast('Erro criação empréstimo', 'error') }
      finally{ setGlobalLoading(false) }
    })
  })

  // Load clients
  async function loadClients(){
    const list = document.getElementById('clients-list')
    list.innerHTML = '<div class="text-sm text-gray-500">Carregando...</div>'
    try{
      const res = await fetch(API + '/clients')
      const data = await res.json()
      list.innerHTML = ''
      const tpl = document.getElementById('client-row')
      data.forEach(c => {
        const node = tpl.content.cloneNode(true)
        node.querySelector('.name').textContent = c.nome
        node.querySelector('.meta').textContent = `${c.cpf_cnpj} • ${c.email} • ${c.telefone}`
        const badge = node.querySelector('.badge')
        // simple badge placeholder
        badge.textContent = c.ativo ? 'Ativo' : 'Inativo'
        badge.classList.add(c.ativo? 'bg-green-100 text-green-800':'bg-gray-100 text-gray-700')
        node.querySelector('.btn-charge').addEventListener('click', ()=>{
          toast('Ação cobrar ainda não implementada', 'info')
        })
        list.appendChild(node)
      })
    }catch(e){ list.innerHTML = '<div class="text-sm text-red-500">Erro ao carregar clientes</div>' }
  }

  // Load loans
  async function loadLoans(){
    const list = document.getElementById('loans-list')
    list.innerHTML = '<div class="text-sm text-gray-500">Carregando...</div>'
    try{
      const res = await fetch(API + '/loans')
      const data = await res.json()
      list.innerHTML = ''
      const tpl = document.getElementById('loan-row')
      data.forEach(l => {
        const node = tpl.content.cloneNode(true)
        node.querySelector('.id').textContent = `${l.id} - R$ ${Number(l.saldo_devedor).toFixed(2)}`
        node.querySelector('.meta').textContent = `Emprestado: R$ ${Number(l.valor_emprestado).toFixed(2)} • ${l.prazo_meses} meses`
        const badge = node.querySelector('.loan-badge')
        const status = (l.saldo_devedor<=0)? 'Quitado' : (new Date().toISOString().slice(0,10) > (l.data_vencimento||'') ? 'Atrasado' : 'Em dia')
        badge.textContent = status
        badge.classList.add(status==='Quitado'?'bg-green-100 text-green-800':status==='Atrasado'?'bg-red-100 text-red-800':'bg-yellow-100 text-yellow-800')

        node.querySelector('.btn-pay').addEventListener('click', ()=> openPaymentModal(l))
        node.querySelector('.btn-details').addEventListener('click', ()=> showLoanDetails(l))
        list.appendChild(node)
      })
    }catch(e){ list.innerHTML = '<div class="text-sm text-red-500">Erro ao carregar empréstimos</div>' }
  }

  function showLoanDetails(loan){
    const modal = document.createElement('div')
    modal.className = 'fixed inset-0 bg-black/40 flex items-center justify-center z-50'
    modal.innerHTML = `
      <div role="dialog" aria-modal="true" class="bg-white rounded p-6 w-full max-w-lg">
        <h3 class="text-lg font-semibold mb-3">Detalhes - ${loan.id}</h3>
        <div class="space-y-2 text-sm">
          <div><strong>Cliente:</strong> ${loan.cliente_id}</div>
          <div><strong>Valor inicial:</strong> R$ ${Number(loan.valor_emprestado).toFixed(2)}</div>
          <div><strong>Saldo devedor:</strong> R$ ${Number(loan.saldo_devedor).toFixed(2)}</div>
          <div><strong>Prazo:</strong> ${loan.prazo_meses} meses</div>
        </div>
        <div class="flex justify-end mt-4"><button id="close-details" class="px-4 py-2 bg-gray-200 rounded">Fechar</button></div>
      </div>`
    modalRoot.appendChild(modal)
    modal.querySelector('#close-details').addEventListener('click', ()=> modal.remove())
  }

  function openPaymentModal(loan){
    const modal = document.createElement('div')
    modal.className = 'fixed inset-0 bg-black/40 flex items-center justify-center z-50'
    modal.innerHTML = `
      <div role="dialog" aria-modal="true" class="bg-white rounded p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-3">Registrar Pagamento - ${loan.id}</h3>
        <form onsubmit="return false;" class="space-y-3">
          <div><label class="block text-sm">Valor sugerido (próxima parcela):<input id="p_valor" class="w-full border rounded px-3 py-2" value="${(loan.valor_parcela||0).toFixed(2)}"></label></div>
          <div><label class="block text-sm">Data<input id="p_data" type="date" class="w-full border rounded px-3 py-2"></label></div>
          <div class="flex justify-end gap-3 mt-4"><button id="cancel-pay" class="px-4 py-2 bg-gray-200 rounded">Cancelar</button><button id="save-pay" class="px-4 py-2 bg-green-600 text-white rounded">Registrar</button></div>
        </form>
      </div>`
    modalRoot.appendChild(modal)
    trapFocus(modal)
    modal.querySelector('#cancel-pay').addEventListener('click', ()=> modal.remove())
    modal.querySelector('#save-pay').addEventListener('click', async ()=>{
      const valor = parseFloat(modal.querySelector('#p_valor').value)
      const data = modal.querySelector('#p_data').value || new Date().toISOString()
      if(!valor || valor<=0){ toast('Valor inválido', 'error'); return }
      setGlobalLoading(true)
      try{
        const res = await fetch(API + '/payments', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({emprestimo_id:loan.id, valor, data})})
        if(res.ok){ toast('Pagamento registrado', 'success'); modal.remove(); await loadLoans() }
        else{ const j = await res.json(); toast('Erro: ' + (j.detail||'falha'), 'error') }
      }catch(e){ toast('Erro ao registrar pagamento', 'error') }
      finally{ setGlobalLoading(false) }
    })
  }

  // Search filters
  clientSearch && clientSearch.addEventListener('input', async (e)=>{
    const q = e.target.value.toLowerCase()
    const items = document.querySelectorAll('#clients-list [role="listitem"]')
    items.forEach(it=>{
      const text = it.innerText.toLowerCase()
      it.style.display = text.includes(q)? '' : 'none'
    })
  })
  loanSearch && loanSearch.addEventListener('input', async (e)=>{
    const q = e.target.value.toLowerCase()
    const items = document.querySelectorAll('#loans-list [role="listitem"]')
    items.forEach(it=>{
      const text = it.innerText.toLowerCase()
      it.style.display = text.includes(q)? '' : 'none'
    })
  })

  // Inicial
  show(loginView)
})();
