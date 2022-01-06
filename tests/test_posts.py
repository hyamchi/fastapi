import pytest
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    # print (res.json())
    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate, res.json())
    posts = list(post_map)
    
    assert res.status_code == 200
    # assert posts[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/50000")
    # print(res.json())
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostOut(**res.json())
    # print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200

@pytest.mark.parametrize("title, content", [
    ("1st tt", "1st cc"), 
    ("2nd tt", "2nd cc"), 
    ("3rd tt", "3rd cc")
    ])
def test_create_post(authorized_client, test_user, test_posts, title, content):
    res = authorized_client.post(f"/posts/", json={"title": title, "content": content})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner_id == test_user['id']
    assert created_post.published == True


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(f"/posts/", json={"title": "tt", "content": "cc"})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    # print(res.json())
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    # print(res.json())
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/10000")
    # print(res.json())
    assert res.status_code == 404

def test_delete__other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    # print(res.json())
    assert res.status_code == 403


def test_create_post(authorized_client, test_user, test_posts):
    data = { 
        "title": "updated title",
        "content": "updated content"
        }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    
def test_update__other_user_post(authorized_client, test_user, test_posts):
    data = { 
        "title": "updated title",
        "content": "updated content"
        }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = { 
        "title": "updated title",
        "content": "updated content"
        }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = { 
        "title": "updated title",
        "content": "updated content"
        }

    res = authorized_client.put(f"/posts/100000", json=data)

    assert res.status_code == 404
