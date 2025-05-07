import asyncio

from sqlalchemy import select

from webapp.core.db.engine import AsyncSessionLocal, engine, Base
from webapp.core.db.models import Location


SEED_DATA = [
    {"post_code": pc, "city": city}
    for pc, city in [
        ("10115", "Berlin"),
        ("20095", "Hamburg"),
        ("80331", "München"),
        ("50667", "Köln"),
        ("60311", "Frankfurt am Main"),
        ("70173", "Stuttgart"),
        ("40213", "Düsseldorf"),
        ("44135", "Dortmund"),
        ("45127", "Essen"),
        ("04109", "Leipzig"),
        ("28195", "Bremen"),
        ("01067", "Dresden"),
        ("30159", "Hannover"),
        ("90402", "Nürnberg"),
        ("47051", "Duisburg"),
        ("44787", "Bochum"),
        ("42103", "Wuppertal"),
        ("33602", "Bielefeld"),
        ("53111", "Bonn"),
        ("48143", "Münster"),
        ("76131", "Karlsruhe"),
        ("68159", "Mannheim"),
        ("86150", "Augsburg"),
        ("65183", "Wiesbaden"),
        ("41061", "Mönchengladbach"),
        ("45879", "Gelsenkirchen"),
        ("38100", "Braunschweig"),
        ("09111", "Chemnitz"),
        ("24103", "Kiel"),
        ("52062", "Aachen"),
        ("06108", "Halle (Saale)"),
        ("39104", "Magdeburg"),
        ("79098", "Freiburg im Breisgau"),
        ("47798", "Krefeld"),
        ("23552", "Lübeck"),
        ("46045", "Oberhausen"),
        ("99084", "Erfurt"),
        ("55116", "Mainz"),
        ("18055", "Rostock"),
        ("34117", "Kassel"),
        ("58095", "Hagen"),
        ("66111", "Saarbrücken"),
        ("59065", "Hamm"),
        ("45468", "Mülheim an der Ruhr"),
        ("14467", "Potsdam"),
        ("67059", "Ludwigshafen am Rhein"),
        ("26122", "Oldenburg"),
        ("51373", "Leverkusen"),
        ("49074", "Osnabrück"),
        ("42651", "Solingen"),
        ("69115", "Heidelberg"),
        ("44623", "Herne"),
        ("41460", "Neuss"),
        ("64283", "Darmstadt"),
        ("33098", "Paderborn"),
        ("93047", "Regensburg"),
        ("85049", "Ingolstadt"),
        ("97070", "Würzburg"),
        ("38440", "Wolfsburg"),
        ("90762", "Fürth"),
        ("89073", "Ulm"),
        ("74072", "Heilbronn"),
        ("75175", "Pforzheim"),
        ("37073", "Göttingen"),
        ("46236", "Bottrop"),
        ("72760", "Reutlingen"),
        ("56068", "Koblenz"),
        ("27568", "Bremerhaven"),
        ("45657", "Recklinghausen"),
        ("51465", "Bergisch Gladbach"),
        ("07743", "Jena"),
        ("91052", "Erlangen"),
        ("42853", "Remscheid"),
        ("47441", "Moers"),
        ("57072", "Siegen"),
        ("31134", "Hildesheim"),
        ("38226", "Salzgitter"),
        ("03046", "Cottbus"),
        ("67655", "Kaiserslautern"),
        ("07545", "Gera"),
        ("58452", "Witten"),
        ("08056", "Zwickau"),
        ("19053", "Schwerin"),
        ("78462", "Konstanz"),
        ("33330", "Gütersloh"),
        ("73728", "Esslingen am Neckar"),
        ("21335", "Lüneburg"),
        ("35037", "Marburg an der Lahn"),
        ("76530", "Baden-Baden"),
        ("95444", "Bayreuth"),
        ("36037", "Fulda"),
        ("94032", "Passau"),
        ("54290", "Trier"),
        ("24534", "Neumünster"),
        ("63065", "Offenbach am Main"),
        ("84028", "Landshut"),
        ("24937", "Flensburg"),
        ("17033", "Neubrandenburg"),
        ("88212", "Ravensburg"),
        ("58507", "Lüdenscheid"),
    ]
]


async def migrate_locations() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Location))
        if result.scalars().first():
            print("Already exists")
            return
        session.add_all(Location(**row) for row in SEED_DATA)
        await session.commit()
        print(f"{len(SEED_DATA)} Locations created.")


if __name__ == "__main__":
    asyncio.run(migrate_locations())
