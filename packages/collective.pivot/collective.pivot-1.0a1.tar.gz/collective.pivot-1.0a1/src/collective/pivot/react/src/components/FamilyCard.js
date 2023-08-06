import React from 'react';

function FamilyCard(props) {

    return(
        <div  style={{  }}   className="offer-card">
            <img className="embed-responsive-img offer-card-img" variant="top" src={"https://pivotweb.tourismewallonie.be/PivotWeb-3.1/img/" + props.item["offer"]["offerID"] } />
            <div className="card-caption">
                <span>{props.item["title"]}</span>
                <a href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]} target="_blank">Détails</a>
            </div>
        </div>
    );
}
export default FamilyCard;