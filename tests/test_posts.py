import pytest
import test
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    """Test creating a post with valid data"""
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client):
    """Test getting all posts without authorization"""
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    """Test getting a single post by ID"""
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_found(authorized_client):
    res = authorized_client.get(f"/posts/{420}")
    assert res.status_code == 404
    assert res.json().get("detail") == "The post with id 420 was not found"

def test_get_one_post(authorized_client, test_posts, test_user):
    """Test getting a single post by ID"""
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    # assert res.json()["Post"]["id"] == test_posts[0].id
    # assert res.json()["Post"]["owner_id"] == test_posts[0].owner_id
    # assert res.json()["Post"]["owner_id"] == test_user["id"]
    # print(res.json())
    post = schemas.PostVoteOut(**res.json())
    assert test_posts[0].id == post.Post.id
    user = post.Post.owner
    assert user.id == test_user["id"]
    assert user.id == test_posts[0].owner_id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("new title 2", "new content 2", False),
    ("new title 3", "new content 3", True),
])

def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json = {"title": title, "content": content, "published": published})
    created_post = schemas.PostOut(**res.json())
    print(created_post)
    assert res.status_code == 201

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json = {"title": "new title", "content": "new content", "published": True})
    assert res.status_code == 401

def test_published_not_given_create_post(authorized_client, test_user):
    res = authorized_client.post("/posts/", json = {"title": "new no publisher", "content": "new content"})
    created_post = schemas.PostOut(**res.json())
    assert res.status_code == 201

def test_delete_post_not_exists(authorized_client):
    res = authorized_client.delete("/posts/1244")
    assert res.status_code == 404
    print(res.json())

def test_unauthorized_deleting_post(client):
    res = client.delete("/posts/1")
    assert res.status_code == 401
    print(res.json())

def test_wrong_user_deleting_post(authorized_client2, test_posts):
    res = authorized_client2.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 403
    print(res.json())

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_not_exist_update_post(authorized_client, test_posts):
    updated_post = {
        "title": "updated post",
        "content": "this is updated",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{3208930}", json = updated_post)
    assert res.status_code == 404

def test_unauthorized_update_post(client, test_posts):
    updated_post = {
        "title": "updated post",
        "content": "this is updated",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json = updated_post)
    assert res.status_code == 401

def test_wrong_user_updating_post(authorized_client2, test_posts):
    updated_post = {
        "title": "updated post",
        "content": "this is updated",
        "id": test_posts[0].id
    }
    res = authorized_client2.put(f"/posts/{test_posts[0].id}", json = updated_post)
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    updated_post = {
        "title": "updated post",
        "content": "this is updated",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = updated_post)
    assert res.status_code == 200
