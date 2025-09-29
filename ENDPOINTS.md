# URLs de la API de Studio Ghibli por Rol

Los usuarios normales tienen acceso limitado a la API de Ghibli basado en su rol asignado:
- `GET /ghibli-api/resources/` - Obtener todos los recursos de su tipo (films, people, etc.)
- `GET /ghibli-api/resources/{id}/` - Obtener recurso específico de su tipo

## URLs por Rol

### Films
`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/films`

`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/films/<id>`

### People
`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/people`

`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/people/<id>`

### Locations
`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/locations`

`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/locations/<id>`

### Species
`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/species`

`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/species/<id>`

### Vehicles
`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/vehicles`

`curl -X GET -H "Content-Type: application/json" https://ghibliapi.vercel.app/vehicles/<id>`
