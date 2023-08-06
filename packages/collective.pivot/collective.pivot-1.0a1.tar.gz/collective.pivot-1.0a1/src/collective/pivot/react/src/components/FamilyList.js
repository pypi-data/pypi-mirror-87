import React, {useState, useEffect} from 'react';
import FamilyCard from './FamilyCard';

function FamilyList(props) {
    const [state, setState] = useState([]);
    const [infoUrl, setInfoUrl] = useState("");

    useEffect(() => {
        setState(props.items)
        setInfoUrl(props.details)

     }, [props])
    return(
        <ul className="pivot-offer-list-container">
           {state && state.map((item, i) => (<li className="pivot-item"><FamilyCard key={i} infoUrl={infoUrl}  item={item}/></li>))}
        </ul>
    );
}

export default FamilyList;