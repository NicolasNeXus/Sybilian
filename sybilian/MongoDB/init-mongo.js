db.createUser(
	{
		user : "TDLOG",
		pwd : "sybilian",
		roles : [
			{
				role : "readWrite",
				db : "sybiliandb"
			}
		]
	}
)
db.createCollection("cards")