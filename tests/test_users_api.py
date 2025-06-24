import requests
import pytest

# Shared variables (can be moved to conftest.py or a config file later)
user_id = "31bno2yjsax5r2snojso47hzpqa4"
playlist_id = "4x8zl54qefqaMQxAQopizn"
sample_playlist = "3cEYpjA9oz9GiPac4AsH4n"
track_uri = "spotify:track:0xN4nwgOWg59k0t94CJAj4"
follow_playlist_id = "4sidrPsqAlSl62HqStcGSa"
artist_ids = ["29aw5YCdIw2FEXYyAJZI8l", "6AiX12wXdXFoGJ2vk8zBjy"]

def test_get_users_top_tracks(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/top/tracks", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

def test_get_users_top_artists(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/top/artists", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

def test_get_current_user_profile(auth_headers, base_url):
    global user_id
    response = requests.get(f"{base_url}/me", headers=auth_headers)
    assert response.status_code == 200
    user_id = response.json()["id"]
    print(response.json())

@pytest.mark.dependency(depends=["test_get_current_user_profile"])
def test_get_user_profile(auth_headers, base_url):
    response = requests.get(f"{base_url}/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

def test_get_current_users_playlists(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/playlists", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.dependency(depends=["test_get_current_user_profile"])
def test_get_users_playlists(auth_headers, base_url):
    response = requests.get(f"{base_url}/users/{user_id}/playlists", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.dependency(depends=["test_get_current_user_profile"])
def test_create_playlist(auth_headers, base_url):
    global playlist_id
    payload = {
        "name": "New Playlist",
        "description": "My new playlist",
        "public": False
    }
    response = requests.post(f"{base_url}/users/{user_id}/playlists", headers=auth_headers, json=payload)
    assert response.status_code == 201
    playlist_id = response.json()["id"]
    print(response.json())

@pytest.mark.dependency(depends=["test_create_playlist"])
def test_get_playlist_cover_image(auth_headers, base_url):
    response = requests.get(f"{base_url}/playlists/{playlist_id}/images", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

def test_get_playlist(auth_headers, base_url):
    response = requests.get(f"{base_url}/playlists/{sample_playlist}", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

def test_change_playlist_details(auth_headers, base_url):
    payload = {
        "name": "New Playlist Name",
        "description": "Updated description",
        "public": False
    }
    response = requests.put(f"{base_url}/playlists/{playlist_id}", headers=auth_headers, json=payload)
    assert response.status_code == 200
    print("Playlist details updated successfully.")

def test_get_playlist_items(auth_headers, base_url):
    response = requests.get(f"{base_url}/playlists/{sample_playlist}/tracks", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

def test_add_items_to_playlist(auth_headers, base_url):
    payload = {
        "uris": [track_uri]
    }
    response = requests.post(f"{base_url}/playlists/{playlist_id}/tracks", headers=auth_headers, json=payload)
    assert response.status_code == 201
    print("Track added successfully.")

def test_remove_playlist_items(auth_headers, base_url):
    payload = {
        "tracks": [{"uri": track_uri}]
    }
    response = requests.delete(f"{base_url}/playlists/{playlist_id}/tracks", headers=auth_headers, json=payload)
    assert response.status_code == 200
    print("Track removed successfully.")

def test_follow_playlist(auth_headers, base_url):
    response = requests.put(
        f"{base_url}/playlists/{follow_playlist_id}/followers",
        headers=auth_headers,
        json={}
    )
    assert response.status_code == 200
    print("Followed playlist successfully!")

def test_unfollow_playlist(auth_headers, base_url):
    response = requests.delete(
        f"{base_url}/playlists/{follow_playlist_id}/followers",
        headers=auth_headers
    )
    assert response.status_code == 200
    print("Unfollowed playlist successfully!")

def test_check_if_user_follows_playlist(auth_headers, base_url):
    response = requests.get(
        f"{base_url}/playlists/{follow_playlist_id}/followers/contains?ids={user_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    print(response.json())

@pytest.mark.order(1)
def test_follow_artists(auth_headers, base_url):
    response = requests.put(
        f"{base_url}/me/following?type=artist",
        headers=auth_headers,
        json={"ids": artist_ids}
    )
    assert response.status_code == 204
    print("Followed artists successfully!")

@pytest.mark.order(2)
def test_check_if_user_follows_artists(auth_headers, base_url):
    ids_param = ",".join(artist_ids)
    response = requests.get(
        f"{base_url}/me/following/contains?type=artist&ids={ids_param}",
        headers=auth_headers
    )
    assert response.status_code == 200
    print(response.json())

@pytest.mark.order(3)
def test_unfollow_artists(auth_headers, base_url):
    response = requests.delete(
        f"{base_url}/me/following?type=artist",
        headers=auth_headers,
        json={"ids": artist_ids}
    )
    assert response.status_code == 204
    print("Unfollowed artists successfully!")

def test_get_followed_artists(auth_headers, base_url):
    response = requests.get(
        f"{base_url}/me/following?type=artist",
        headers=auth_headers
    )
    assert response.status_code == 200
    print(response.json())

episode_id = "1yt4xdNIPiuWPnbhHWjSuj"
episode_ids = "512ojhOuo1ktJprKbVcKyQ,77o6BIVlYM3msb4MMIL1jH"

def test_get_episode(auth_headers, base_url):
    response = requests.get(f"{base_url}/episodes/{episode_id}", headers=auth_headers)
    assert response.status_code == 200
    print("Episode Info:", response.json())

def test_get_several_episodes(auth_headers, base_url):
    response = requests.get(f"{base_url}/episodes", headers=auth_headers, params={"ids": episode_ids})
    assert response.status_code == 200
    print("Several Episodes Info:", response.json())

def test_get_users_saved_episodes(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/episodes", headers=auth_headers)
    assert response.status_code == 200
    print("User's Saved Episodes:", response.json())

def test_save_episodes_for_user(auth_headers, base_url):
    response = requests.put(f"{base_url}/me/episodes", headers=auth_headers, params={"ids": episode_ids})
    assert response.status_code == 200
    print("Episodes saved successfully.")

def test_remove_users_saved_episodes(auth_headers, base_url):
    response = requests.delete(f"{base_url}/me/episodes", headers=auth_headers, params={"ids": episode_ids})
    assert response.status_code == 200
    print("Episodes removed successfully.")

def test_check_users_saved_episodes(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/episodes/contains", headers=auth_headers, params={"ids": episode_ids})
    assert response.status_code == 200
    print("Saved Episodes Check:", response.json())

device_id = "74ASZWbe4lXaubB36ztrGX"

def test_get_available_markets(auth_headers, base_url):
    response = requests.get(f"{base_url}/markets", headers=auth_headers)
    assert response.status_code == 200
    print("Available Markets:", response.json())

def test_get_playback_state(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/player", headers=auth_headers)
    assert response.status_code == 200
    print("Playback State:", response.json())

def test_transfer_playback(auth_headers, base_url):
    payload = {
        "device_ids": [device_id],
        "play": True
    }
    response = requests.put(f"{base_url}/me/player", headers=auth_headers, json=payload)
    assert response.status_code == 204
    print("Playback transferred successfully.")

def test_get_available_devices(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/player/devices", headers=auth_headers)
    assert response.status_code == 200
    print("Available Devices:", response.json())

def test_get_currently_playing_track(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/player/currently-playing", headers=auth_headers)
    assert response.status_code in [200, 204]
    print("Currently Playing Track:", response.text)

def test_start_resume_playback(auth_headers, base_url):
    payload = {"device_id": device_id}
    response = requests.put(f"{base_url}/me/player/play", headers=auth_headers, json=payload)
    assert response.status_code in [204, 403]
    print("Playback started/resumed.")

def test_pause_playback(auth_headers, base_url):
    response = requests.put(f"{base_url}/me/player/pause", headers=auth_headers)
    assert response.status_code in [204, 403]
    print("Playback paused.")

def test_skip_to_next(auth_headers, base_url):
    response = requests.post(f"{base_url}/me/player/next", headers=auth_headers)
    assert response.status_code == 204
    print("Skipped to next track.")

show_id = "38bS44xjbVVZ3No3ByF1dJ"
show_ids = "5CfCWKI5pZ28U0uOzXkDHe,2C5as3aKmN2k11yfDDDSrvaZ"

def test_search_for_item(auth_headers, base_url):
    query = "Ed Sheeran"
    search_type = "artist"
    params = {"q": query, "type": search_type}
    response = requests.get(f"{base_url}/search", headers=auth_headers, params=params)
    assert response.status_code == 200
    print("Search Results:", response.json())

def test_get_show(auth_headers, base_url):
    response = requests.get(f"{base_url}/shows/{show_id}", headers=auth_headers)
    assert response.status_code == 200
    print("Show Details:", response.json())

def test_get_several_shows(auth_headers, base_url):
    response = requests.get(f"{base_url}/shows", headers=auth_headers, params={"ids": show_ids})
    assert response.status_code == 200
    print("Multiple Shows Details:", response.json())

def test_get_show_episodes(auth_headers, base_url):
    response = requests.get(f"{base_url}/shows/{show_id}/episodes", headers=auth_headers)
    assert response.status_code == 200
    print("Show Episodes:", response.json())

def test_get_users_saved_shows(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/shows", headers=auth_headers)
    assert response.status_code == 200
    print("User's Saved Shows:", response.json())

def test_save_shows_for_user(auth_headers, base_url):
    response = requests.put(f"{base_url}/me/shows", headers=auth_headers, params={"ids": show_id})
    assert response.status_code == 200
    print("Shows saved successfully.")

def test_remove_users_saved_shows(auth_headers, base_url):
    response = requests.delete(f"{base_url}/me/shows", headers=auth_headers, params={"ids": show_id})
    assert response.status_code == 200
    print("Shows removed successfully.")

def test_check_users_saved_shows(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/shows/contains", headers=auth_headers, params={"ids": show_id})
    assert response.status_code == 200
    print("Check Saved Shows:", response.json())

show_id = "38bS44xjbVVZ3No3ByF1dJ"
show_ids = "5CfCWKI5pZ28U0uOzXkDHe,2C5as3aKmN2k11yfDDDSrvaZ"

def test_search_for_item(auth_headers, base_url):
    query = "Ed Sheeran"
    search_type = "artist"
    params = {"q": query, "type": search_type}
    response = requests.get(f"{base_url}/search", headers=auth_headers, params=params)
    assert response.status_code == 200
    print("Search Results:", response.json())

def test_get_show(auth_headers, base_url):
    response = requests.get(f"{base_url}/shows/{show_id}", headers=auth_headers)
    assert response.status_code == 200
    print("Show Details:", response.json())

def test_get_several_shows(auth_headers, base_url):
    response = requests.get(f"{base_url}/shows", headers=auth_headers, params={"ids": show_ids})
    assert response.status_code == 200
    print("Multiple Shows Details:", response.json())

def test_get_show_episodes(auth_headers, base_url):
    response = requests.get(f"{base_url}/shows/{show_id}/episodes", headers=auth_headers)
    assert response.status_code == 200
    print("Show Episodes:", response.json())

def test_get_users_saved_shows(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/shows", headers=auth_headers)
    assert response.status_code == 200
    print("User's Saved Shows:", response.json())

def test_save_shows_for_user(auth_headers, base_url):
    response = requests.put(f"{base_url}/me/shows", headers=auth_headers, params={"ids": show_id})
    assert response.status_code == 200
    print("Shows saved successfully.")

def test_remove_users_saved_shows(auth_headers, base_url):
    response = requests.delete(f"{base_url}/me/shows", headers=auth_headers, params={"ids": show_id})
    assert response.status_code == 200
    print("Shows removed successfully.")

def test_check_users_saved_shows(auth_headers, base_url):
    response = requests.get(f"{base_url}/me/shows/contains", headers=auth_headers, params={"ids": show_id})
    assert response.status_code == 200
    print("Check Saved Shows:", response.json())

