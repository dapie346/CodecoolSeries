let firstPageRun = true;

if (firstPageRun) {
    window.onload = function init() {
        generateTable(1)
            .then(
                addListeners()
            );
    }
}

async function addListeners() {
    const columns = document.querySelectorAll('th.column');
    columns.forEach(column  => {
        column.addEventListener('click', async () => {
            if (column.classList.contains('sorting-type')){
                if (column.classList.contains('descending')){
                    column.classList.remove('descending');
                    column.classList.add('ascending');
                }
                else if (column.classList.contains('ascending')){
                    column.classList.remove('ascending');
                    column.classList.add('descending');
                }
            }
            else {
                document.querySelector('.sorting-type').classList.remove('sorting-type');
                column.classList.add('sorting-type');
                column.classList.add('descending');
            }
            let page = getActivePageNumber();
            await generateTable(String(page))
        });
    });
    const pagination = document.querySelectorAll('.pagination li');
    pagination.forEach(paginationPage  => {
        paginationPage.addEventListener('click', async () => {
            let clickedPage = paginationPage.innerHTML;
            let page;
            if (clickedPage === '&lt;&lt;'){
                page = Number(getActivePageNumber()) - 1;
            }
            else if (clickedPage === '&gt;&gt;'){
                page = Number(getActivePageNumber()) + 1;

            }
            else {
                page = clickedPage;
            }
            document.querySelector('.active').classList.remove('active');
            await generateTable(String(page));
        });
    });
}

function getActivePageNumber() {
    return document.querySelector('.active').innerHTML;
}

async function generateTable(page){
    let sorting_order;



    let shows;
    let sorting_type;
    let order_mark;
    if (!firstPageRun) {
        sorting_type = document.querySelector('.sorting-type').id;
        if (document.querySelector('.sorting-type').classList.contains('descending')) {
            sorting_order = 'descending';
            order_mark = '  ⇧';
        }
        else {
            sorting_order = 'ascending';
            order_mark = '  ⇩';
        }
    }
    else {
        sorting_type = 'rating';
        sorting_order = 'descending'
        order_mark = '  ⇧';
    }
    shows = await getShows(sorting_type);
    if (sorting_order === 'ascending'){
        shows.reverse();
    }
    const shows_total = shows.length;
    const shows_per_page = 15;



    let paginatedShows = getPaginatedShows(page, shows, shows_per_page);
    let tableContent = `<tr>
            <th class="column" id="title">Title</th>
            <th class="column" id="year">Year</th>
            <th class="column" id="runtime">Runtime (min)</th>
            <th class="column`
    if (firstPageRun) {
        tableContent += ` sorting-type descending`
        firstPageRun = false;
    }
    tableContent += `" id="rating">Rating</th>
            <th>Genres</th>
            <th>Trailer</th>
            <th>Homepage</th>
            <th class="action-column">Actions</th>
        </tr>`

    paginatedShows.forEach(show=> {
        if (show) {
        tableContent += `<tr id="shows">
            <td><a href="/show/${show.show_id}">${show.title}</a></td>
            <td>${show.year}</td>
            <td>${show.runtime}</td>
            <td>${show.rating}</td>
            <td>${show.genres}</td>
            <td>`;
        if (show.trailer){
            tableContent += `<a href="${show.trailer}">Link</a>`;
        }
        else{
            tableContent += `No URL`;
        }
        tableContent += `</td>
            <td>`;
        if (show.homepage) {
            tableContent += `<a href="${show.homepage}">Link</a>`;
        }
        else{
            tableContent += `No URL`;
        }
        tableContent += `</td>
            <td class="action-column">
                <button type="button" class="icon-button"><i class="fa fa-edit fa-fw"></i></button>
                <button type="button" class="icon-button"><i class="fa fa-trash fa-fw"></i></button>
            </td>
        </tr>`
        }
    })

    let paginationContent = `<ul class="pagination">
            <li `
    if (Number(page) === 1) {
        paginationContent +=`style="display: none;"`
    }
    paginationContent +=`><<</li>`
    for (let number = 1; number < (shows_total / shows_per_page + 1); number++) {
        if (number >= (Number(page) - 2) && number <= (Number(page) + 2)) {
            paginationContent +=`<li>${number}</li>`
        }
    }
    paginationContent +=`<li `
    if (Number(page) >= (shows_total / shows_per_page)){
        paginationContent +=`style="display: none;"`
    }
    paginationContent += `>>></li></div>`


    document.getElementById("table").innerHTML = "";
    document.getElementById("table").innerHTML = tableContent;
    document.getElementById("pagination").innerHTML = "";
    document.getElementById("pagination").innerHTML = paginationContent;

    const pagination = document.querySelectorAll('.pagination li');
    pagination.forEach(paginationPage  => {
        if (paginationPage.innerText === String(page)) {
            paginationPage.classList.add('active');
        }
    })
    let columns = document.querySelectorAll('th.column');
    columns.forEach(column  => {
        if (column.id === sorting_type) {
            column.classList.add('sorting-type');
            column.classList.add(sorting_order);
            column.innerHTML += order_mark;
        }
    })


    addListeners()
}

function getPaginatedShows(page, shows, shows_per_page) {
  shows.forEach(show => {
    show.rating = show.rating.toString().slice(0, 3);
    show.year = show.year.toString().slice(12, 16);
  });
  let start = (Number(page) - 1) * shows_per_page;
  let end = Number(page) * shows_per_page;
  return shows.slice(start, end);
}


async function getShows(sorting_type) {
        return await apiGet(`/shows/${sorting_type}/`)
    }

async function apiGet(url) {
    let response = await fetch(url, {
        method: "GET",
    });
    if (response.ok) {
        return await response.json()
    }
}

