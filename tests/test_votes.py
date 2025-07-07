import pytest
import test
from app import model, schemas
from tests import test_posts
from tests.conftest import authorized_client

@pytest.fixture()
def testing_vote(test_posts, test_user, session):
    new_vote = model.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_unauthorized_voter(client):
    vote = {
        "post_id": 1,
        "vote_dir": 1,
    }
    res = client.post("/vote/", json = vote)
    assert res.status_code == 401

def test_post_not_exist(authorized_client, test_posts):
    vote = {
        "post_id": 32049,
        "vote_dir": 1,
    }
    res = authorized_client.post("/vote/", json = vote)
    assert res.status_code == 404

def test_already_voted(authorized_client, test_posts, testing_vote):
    vote = {
        "post_id": test_posts[0].id,
        "vote_dir": 1,
    }
    res = authorized_client.post("/vote/", json = vote)
    assert res.status_code == 409

def test_vote_does_not_exist(authorized_client, test_posts, testing_vote):
    vote = {
        "post_id": test_posts[1].id,
        "vote_dir": 0,
    }
    res = authorized_client.post("/vote/", json = vote)
    assert res.status_code == 404

def test_vote_remove(authorized_client, test_posts, testing_vote):
    vote = {
        "post_id": test_posts[0].id,
        "vote_dir": 0,
    }
    res = authorized_client.post("/vote/", json = vote)
    assert res.status_code == 204


def test_vote(authorized_client, test_posts):
    vote = {
        "post_id": test_posts[0].id,
        "vote_dir": 1,
    }
    res = authorized_client.post("/vote/", json = vote)
    assert res.status_code == 201
