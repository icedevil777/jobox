function handleFormSubmit(event) {
  // Просим форму не отправлять данные самостоятельно
  event.preventDefault()
  console.log('Отправка!')
}

const applicantForm = document.getElementById('mars-once')
applicantForm.addEventListener('submit', handleFormSubmit)



function serializeForm(formNode) {
  console.log(formNode.elements)
}

function handleFormSubmit(event) {
  event.preventDefault()
  serializeForm(applicantForm)
}

const applicantForm = document.getElementById('mars-once')
applicantForm.addEventListener('submit', handleFormSubmit)

function serializeForm(formNode) {
  const { elements } = formNode

  Array.from(elements)
    .forEach((element) => {
      const { name, value } = element
      console.log({ name, value })
    })
}

function serializeForm(formNode) {
  const { elements } = formNode
  const data = Array.from(elements)
    .filter((item) => !!item.name)
    .map((element) => {
      const { name, value } = element

      return { name, value }
    })

  console.log(data)
}

const isOn = someCheckboxInput.checked


function serializeForm(formNode) {
  const { elements } = formNode

  const data = Array.from(elements)
    .map((element) => {
      const { name, type } = element
      const value = type === 'checkbox' ? element.checked : element.value

      return { name, value }
    })
    .filter((item) => !!item.name)

  console.log(data)
}

function serializeForm(formNode) {
  const { elements } = formNode

  const data = new FormData()

  Array.from(elements)
    .filter((item) => !!item.name)
    .forEach((element) => {
      const { name, type } = element
      const value = type === 'checkbox' ? element.checked : element.value

      data.append(name, value)
    })

  return data
}
