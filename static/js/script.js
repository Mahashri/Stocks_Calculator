// Autocomplete function for the stock symbol input
function autocomplete(inp, arr) {
    var currentFocus;

    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        for (i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                    updateStockLogo(inp.value); // Update logo on selection
                });
                a.appendChild(b);
            }
        }
    });

    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) {
            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

// Function to update the stock logo based on the selected symbol
function updateStockLogo(symbol) {
    var token = 'pk_bVnOe_jqR5ymzQIbVbAr8Q';
    var logoUrl = `https://img.logo.dev/${symbol}.com?token=${token}`;
    document.getElementById('stock_logo').src = logoUrl;
}

// Predefined list of stocks
var nifty50Stocks = [
    // Nifty 50
"ABB","ABFRL","AIAENG","ADANIGREEN","ADANIPORTS","ADANIPOWER","ADITYABIRLA","ADITYABIRLAC","ADITYABIRLACEM","ADITYABIRLAHL","AMBUJACEM","ARVIND","ASIANPAINT","AUROPHARMA","AUBANK","AXISBANK","BAJAJAUTO","BAJFINANCE","BAJAJFINSV","BAJAJHLDNG","BANKBARODA","BANKINDIA","BANDHANBNK","BEL","BEML","BERGEPAINT","BIOCON","BIRLAHT","BPCL","BRIGADE","BRITANNIA","CADILAHC","CASTROLIND","CEATLTD","CENTRALBK","CENTURYPLY","CEAT","COLPAL","CONCOR","COROMANDEL","CUMMINSIND","CUB","DABUR","DALBHARAT","DEEPAKNTR","DIVISLAB","DLF","DMART","DRREDDY","EDELWEISS","EICHERMOT","FEDERALBNK","GAIL","GILLETTE","GLENMARK","GODREJCP","GODREJIND","HCLTECH","HDFCBANK","HDFCAMC","HDFCLIFE","HINDALCO","HINDUNILVR","HPCL","HIL","HINDASTAL","IDFC","IDFCFIRSTB","IDBI","IGL","INDIAMART","INDUSINDBK","INFY","INFRATEL","IRCTC","ISGEC","INDHOTEL","J&KBANK","JKTYRE","JINDALPOLY","JINDALSAW","JINDALSTEL","JINDALWORLD","JSWENERGY","JSWSTEEL","JSWINFRA","JSWHL","JSWISPL","JUBLFOOD","KARURVYSYA","KOTAKBANK","LARSEN","LICHSGFIN","LUPIN","M&M","MAHINDCIE","MAHINDRA","MAHINDRALOG","MANAPPURAM","MARICO","MARUTI","MCDOWELL-N","MGL","MAXFIN","MUTHOOTFIN","MBECL","NATIONALUM","NESTLEIND","NHPC","NTPC","ONGC","PAGEIND","PFC","PIDILITIND","POWERGRID","RECLTD","RELIANCE","RELIANCEINFRA","RDFCL","RBLBANK","RSWM","SAIL","SBIN","SBILIFE","SHREECEM","SUNPHARMA","SUNTV","TATAELXSI","TATACONSUM","TATACHEM","TATAMETALI","TATAMOTORS","TATASTEEL","TATAPOWER","TATATECH","TECHM","TRENT","UPL","ULTRACEMCO","VEDL","VSTIND","WELLS","WIPRO","YESBANK","ZOMATO","ZYDUSWELL","MAZDOCK","COCHINSHIP","OLAELEC","TVSMOTOR","SOUTHBANK","KALYANKJIL"
,"BAJAJHFL","RAJESHEXPO"




];

// Initialize autocomplete functionality
autocomplete(document.getElementById("stock_symbol"), nifty50Stocks);

// Set default date range on page load
window.onload = function() {
    var today = new Date();
    var yearAgo = new Date();
    yearAgo.setFullYear(today.getFullYear() - 1);

    var formatDate = function(date) {
        var day = ("0" + date.getDate()).slice(-2);
        var month = ("0" + (date.getMonth() + 1)).slice(-2);
        return date.getFullYear() + "-" + month + "-" + day;
    };

    document.getElementById('start_date').value = formatDate(yearAgo);
    document.getElementById('end_date').value = formatDate(today);
};

// Validate dates before form submission
document.querySelector("form").onsubmit = function() {
    var startDate = new Date(document.getElementById("start_date").value);
    var endDate = new Date(document.getElementById("end_date").value);
    if (startDate > endDate) {
        alert("End date must be after the start date.");
        return false;
    }
    return true;
};
