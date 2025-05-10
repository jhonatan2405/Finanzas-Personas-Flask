// Scripts personalizados para el Sistema de Finanzas Personales

// Función para formatear números como moneda
function formatCurrency(amount) {
  return new Intl.NumberFormat("es-MX", {
    style: "currency",
    currency: "MXN",
    minimumFractionDigits: 2,
  }).format(amount)
}

// Función para validar formularios
function validateForm(formId) {
  const form = document.getElementById(formId)

  if (!form) return true

  // Validar campos requeridos
  const requiredFields = form.querySelectorAll("[required]")
  let isValid = true

  requiredFields.forEach((field) => {
    if (!field.value.trim()) {
      field.classList.add("is-invalid")
      isValid = false
    } else {
      field.classList.remove("is-invalid")
    }
  })

  // Validar monto
  const montoField = form.querySelector("#monto")
  if (montoField && montoField.value <= 0) {
    montoField.classList.add("is-invalid")
    isValid = false
  }

  return isValid
}

// Inicializar tooltips de Bootstrap
document.addEventListener("DOMContentLoaded", () => {
  // Inicializar tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Agregar validación a los formularios
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!validateForm(form.id)) {
        event.preventDefault()
        event.stopPropagation()
      }
    })
  })

  // Establecer fecha actual en campos de fecha si no tienen valor
  const dateInputs = document.querySelectorAll('input[type="date"]')
  dateInputs.forEach((input) => {
    if (!input.value) {
      const today = new Date()
      const year = today.getFullYear()
      let month = today.getMonth() + 1
      let day = today.getDate()

      month = month < 10 ? "0" + month : month
      day = day < 10 ? "0" + day : day

      input.value = `${year}-${month}-${day}`
    }
  })

  // Initialize Bootstrap components after the DOM is fully loaded
  const initializeBootstrap = () => {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    tooltipTriggerList.forEach((tooltipTriggerEl) => {
      new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Initialize popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    popoverTriggerList.forEach((popoverTriggerEl) => {
      new bootstrap.Popover(popoverTriggerEl)
    })
  }

  initializeBootstrap()
})

// Función para confirmar eliminación
function confirmarEliminacion(mensaje) {
  return confirm(mensaje || "¿Estás seguro de que deseas eliminar este elemento?")
}
