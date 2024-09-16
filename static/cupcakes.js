const BASE_URL = 'http://127.0.0.1:5000/api/';
const $allCupcakes = $("#cupcakes");
let cupcakes;

class Cupcake {
    // constructor(cupcakeObj) {
    //     for (let prop in cupcakeObj) {
    //         this[prop] = cupcakeObj[prop];
    //     }
    // }
    
    constructor({id, flavor, size, rating, image}) {
        this.id = id;
        this.flavor = flavor;
        this.size = size;
        this.rating = rating;
        this.image = image;
    }

    static async createCupcakes(cupcakeObj){
        const response = await axios.post(`${BASE_URL}cupcakes`, cupcakeObj);
    }
}

class CupcakeList {
    constructor(cupcakes) {
        this.cupcakes = cupcakes;
    }

    static async fetchAllCupcakes() {
        const response = await axios({
            url: `${BASE_URL}cupcakes`,
            method: "GET"
        })

        const cupcakes = response.data.cupcakes.map(cupcake => new Cupcake(cupcake));

        return new CupcakeList(cupcakes);
    }
}

function generateCupcakeMarkup(cupcake) {
    return $(`
        <div class="col-4 mb-3">
            <img src="${cupcake.image}" alt="An image of the cupcake" width="300" height="500"><br>
            <b>Flavor:</b> ${cupcake.flavor} <br>
            <b>Size:</b> ${cupcake.size} <br>
            <b>Rating:</b> ${cupcake.rating}
        </div>
        `);
}

function showCupcakes(cupcakeArray) {
    console.log("Showing cupcakes on home page ...")
    $allCupcakes.empty();

    for (let cupcake of cupcakeArray) {
        const $cupcake = generateCupcakeMarkup(cupcake);
        $allCupcakes.append($cupcake);
    }
}

async function start() {
    console.log("Getting all cupcakes ...")

    cupcakes = await CupcakeList.fetchAllCupcakes();

    showCupcakes(cupcakes.cupcakes);
}

$(start);

async function handleAddCupcake(evt) {
    evt.preventDefault();
    
    const flavor = $("#flavor").val();
    const size = $("#size").val() === '1' ? "small" : "large";
    const rating = $("#rating").val();
    const image = $("#image").val() === '' ? null : $("#image").val();
    await Cupcake.createCupcakes({flavor, size, rating, image});
    
    evt.target.reset();
    $(start);
}
$("#add-cupcake").on("submit", handleAddCupcake);
