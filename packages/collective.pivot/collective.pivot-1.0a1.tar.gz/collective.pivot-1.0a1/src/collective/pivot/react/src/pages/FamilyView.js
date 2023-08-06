import React, {useState, useEffect} from 'react';
import FamilyFilter from '../components/FamilyFilter';
import FamilyList from '../components/FamilyList';
import FamilyMap from '../components/FamilyMap';

function FamilyView({pivot_url, details_url}) {
  const [categoryList, setCategoryList] = React.useState([]);
  const [items, setItems] = useState([]);
  const [activeCategory, setActiveCategory] = React.useState("null");
  const [filterItems, setFilterItems] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = React.useState(null);
  
  const myHeaders = new Headers();
  myHeaders.append("Accept", "application/json");
  const requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };

  // fetch data 
  const useFetch = (url, options, stateSetter) => {
    let ignore = false;
    React.useEffect(() => {
      const fetchData = async () => {
        try {
          setLoading(true);
          setError({});
          const res = await fetch(url, options);
          const json = await res.json();
          if (!ignore) stateSetter(json.items);
          
        } catch (error) {
          setError(error);
        }
        setLoading(false);
      };
      fetchData();
      return (() => { ignore = true; });
    }, []);
  };

  useFetch(pivot_url, requestOptions, setItems);

  // fetch category
  useEffect(() => {
    async function getCharacters() {
      const response = await fetch(pivot_url, requestOptions);
      const body = await response.json();
      setCategoryList( () => {
          let category = body.items.map(t => t.offer.offerTypeLabel)
          let filter =  category.filter((value, index) => {return category.indexOf(value) === index;})
          return filter
      });
    }
    getCharacters();
  }, []);


    useEffect(() => {
      if(activeCategory !== "null"){
        const f = items.filter(item => item.offer.offerTypeLabel === activeCategory);
        setFilterItems(f);
      }else{
        setFilterItems(items)
        
      }
    }, [activeCategory,items]);

    function handleCategory(newCategory) {
        setActiveCategory(newCategory);
      }

    return(
      <div className="pivot-container">
        {loading ? (
          "Loading..."
        ) : (
          <div>
            <div className="pivot-result">
              <div className="pivot-offer-list">
              <div className="pivot-filter">
              <FamilyFilter items={items} category={categoryList} value={activeCategory} onChange={handleCategory} />
              <span className="pivot-result-count">Il y a {filterItems && filterItems.length} offres</span>
            </div>
                <FamilyList details={details_url} items={filterItems} />
              </div>
              <div className="pivot-offer-map"><FamilyMap details={details_url} items={filterItems}/></div>
            </div>
          </div>
          )}
      </div>
    )
}

export default FamilyView;