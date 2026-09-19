You are helping the user interact with their Jellyfin instance at https://jellyfin.milopolis.org via its REST API.

## Getting the API key

The API key lives in 1Password at `op://git-secrets/jellyfin/api-key`. Fetch it at the start of every session:

```bash
JELLYFIN_API_KEY=$(op read "op://git-secrets/jellyfin/api-key")
```

Also fetch the user ID if you need user-specific endpoints (favorites, played status, etc.):

```bash
JELLYFIN_USER_ID=$(op read "op://git-secrets/jellyfin/user-id")
```

Use `X-Emby-Token: $JELLYFIN_API_KEY` as the auth header on every request.

Base URL: `https://jellyfin.milopolis.org`

## Common operations

### Search / find items

```bash
# Search by name
curl -s -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Items?searchTerm=TITLE&includeItemTypes=Movie,Series&recursive=true" \
  | jq '.Items[] | {Id, Name, Type}'

# Get a single item by ID
curl -s -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Items/ITEM_ID" | jq .
```

### Update item metadata

Jellyfin requires a full round-trip: fetch the item, mutate fields, POST it back.

```bash
# Fetch
ITEM=$(curl -s -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Items/ITEM_ID")

# Mutate with jq, then POST back
echo "$ITEM" | jq '.Overview = "New overview text"' | \
  curl -s -X POST \
    -H "X-Emby-Token: $JELLYFIN_API_KEY" \
    -H "Content-Type: application/json" \
    -d @- \
    "https://jellyfin.milopolis.org/Items/ITEM_ID"
```

Writable fields include: `Name`, `OriginalTitle`, `ForcedSortName`, `Overview`, `Taglines`, `Genres`, `Tags`, `Studios`, `ProductionYear`, `PremiereDate`, `CommunityRating`, `CriticRating`, `OfficialRating`, `CustomRating`, `People`, `ProviderIds`.

### Add/remove tags (bulk)

Always lock the Tags field in the same POST that writes tags. This prevents metadata refreshes from overwriting manually set tags.

Use the **minimal payload pattern** (learned from jellytags). Fetch only `Tags,Genres,ProviderIds` — do NOT include `Overview` or other text fields, as Jellyfin sometimes emits malformed JSON (unescaped quotes, NaN values) in those fields. The POST endpoint accepts a partial BaseItemDto.

```bash
# Search by tag
curl -s -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Items?tags=christmas&includeItemTypes=Movie&recursive=true" \
  | jq '.Items[] | {Id, Name}'

# Add a tag to one item — fetch minimal fields, post minimal payload + lock
ITEM=$(curl -s -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Items?ids=ITEM_ID&userId=$JELLYFIN_USER_ID&fields=Tags,Genres,ProviderIds")

echo "$ITEM" | jq '.Items[0] | {
  Id,
  Name,
  Tags: ((.Tags // []) + ["newtag"] | unique),
  Genres: (.Genres // []),
  ProviderIds: (.ProviderIds // {})
}' | curl -s -X POST \
  -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- \
  "https://jellyfin.milopolis.org/Items/ITEM_ID"
```

Note: the minimal payload approach does not carry `LockedFields` through the fetch (it's not returned in the base fields). To also lock, add it to the jq payload:

```jq
.LockedFields = ["Tags"]
```

The `| unique` on `LockedFields` prevents duplicates if the field was already locked.

### Refresh metadata from providers

```bash
# Refresh a single item (pulls from TMDB/TVDB/etc.)
curl -s -X POST \
  -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Items/ITEM_ID/Refresh?metadataRefreshMode=FullRefresh&imageRefreshMode=FullRefresh&replaceAllMetadata=false"
```

### Library scan

```bash
curl -s -X POST \
  -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Library/Refresh"
```

### User data (played status, favorites)

```bash
# Mark as played
curl -s -X POST \
  -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Users/$JELLYFIN_USER_ID/PlayedItems/ITEM_ID"

# Mark as favorite
curl -s -X POST \
  -H "X-Emby-Token: $JELLYFIN_API_KEY" \
  "https://jellyfin.milopolis.org/Users/$JELLYFIN_USER_ID/FavoriteItems/ITEM_ID"
```

## Workflow for bulk operations

For any bulk update, follow this pattern:
1. Use the search endpoint to get a list of item IDs matching your criteria
2. Show the user the list and confirm before making changes
3. Loop through IDs, applying the update to each
4. Report success/failure counts when done

Always confirm with the user before modifying more than a handful of items.
