mailman2discourse is a **command line tool to import a `mailman2`
configuration (as found in the `config.pck` file) into a discourse
category**. A user is created for each member of the mailing list and
they are notified when a new message is posted to the category (unless
their mailman2 option was to never receive any mail). The moderators
of a private mailing list become members of a discourse group who [can
review every new
post](https://meta.discourse.org/t/category-group-review-moderation/116478).
If the archives of the mailing list are not public, the discourse
category is only visible to a discourse group mimicing the mailman2
membership list. The details of the conversion are explained below.

Install
=======

* apt-get install pipenv python3-dev
* pipenv install mailman2discourse

Usage
=====

Requirements:

* API Key (from `/admin/api/keys/new`) with a `User Level` of `All Users`
* An admin user (for instance `admin`)
* An [mbox importer](https://meta.discourse.org/t/importing-mailing-lists-mbox-listserv-google-groups-emails/79773) container with
  * `DISCOURSE_MAX_ADMIN_API_REQS_PER_KEY_PER_MINUTE: 60000000`
  * `DISCOURSE_MAX_REQS_PER_IP_MODE: none`
* The `config.pck` file of the mailing2 mailing list

To import the `listname@example.com` mailman2 mailing list:

    mailman2discourse --url http://172.19.0.2 --api-key APIKEY --api-user admin \
                      --mailman-config config.pck \
                      --list listname --domain example.com

The content of the archives can then be imported.

Archive import
==============

The mailing list archives can be imported using the [mbox
importer](https://meta.discourse.org/t/importing-mailing-lists-mbox-listserv-google-groups-emails/79773).
The `.mbox` and `.mbox.gz` must be placed in a directory that has the
same name as the category created by `mailman2discourse`.

Details of the config.pck conversion into discourse
===================================================

Category
--------

For a given list (`thelist`), a discourse category is created by the same name.

* mailling list email: copied to **email_in**
* **description**: overrides the content of the message at **topic_url**, only if
  it is more than 5 characters long

Users
-----

* **private_roster** is `1/members` or `2/admins`: user preference **hide_profile_and_presence** = `true`
* **delivery_status** is `0`, empty string or absent: **notification_level** = `3/Wachting` on the `thelist` category
* **delivery_status** is not `0`: **notification_level** = `0/Muted` on the `thelist` category
* **language**: copied to user preference **locale**
* **usernames**: discarded. If the subscriber never posted to the
   list, their membership never was public. If the subscriber posted
   to the list, it is possible they used a name that is different
   and do not want the name used to subscribe to the list to be
   made public.

Groups
------

The `thelist-moderators` group is created and its members are the owners
of the mailing list. The group access is set to allow users to leave
the group freely (**group[public_exit]** = 'true'). If the mailing list is moderated, it is set to be
the [moderation group of the
category](https://meta.discourse.org/t/category-group-review-moderation/116478).
If the mailing list is not moderated, the members of `thelist-moderators` do not
have any control over the category, they are only a reminder of who were
the owners of the mailing list prior to the migration to discourse.

* **owner**: they are made owners of the `thelist-moderators` group
* **moderator**: they are made members of the `thelist-moderators` group, if it exists.

The `thelist-members` group is created, for membership purposes,
unless the mailing list has public archives and anyone can subscribe
without the approval of a moderator. The owners of the
`thelist-moderators` group are also owners of the `thelist-members`
group. The group access is set to allow users to leave the group freely (**group[public_exit]** = 'true').

* **owner**: they are made owners of the `thelist-members` group if it exists
* **member**: they are made members of the `thelist-members` group, if it exists.

The rules for users to join the `thelist-moderators` group is
set depending on the **private_roster** field from `config.pck`.

* **private_roster** is `0/public`:
  * **group[members_visibility_level]** = `0/Everyone`
  * **group[visibility_level]** = `0/Everyone`
* **private_roster** is `1/members`:
  * **group[members_visibility_level]** = `2/Members`
  * **group[visibility_level]** = `0/Everyone`
* **private_roster** is `2/admins`:
  * **group[members_visibility_level]** = `3/Group owners and staff`
  * **group[visibility_level]** = `0/Everyone`

And group members must be added by the group owners, it is not open to
anyone and membership cannot be requested. It is assumed that a
preliminary dialog with the moderators has to take place before they
are accepted. In mailman there is no process to request to become a
mailing list owner.

* **group[public_admission]** = 'false'
* **group[allow_membership_requests]** = 'false'

The `thelist-members` group members visibility and subscription is set depending on the
**private_roster** and **subscribe_policy** fields from `config.pck`.

* **private_roster** is `0/public` and **subscribe_policy** is `0/open` or `1/confirm`:
  * **group[public_admission]** = 'true'
  * **group[allow_membership_requests]** = 'false'
  * **group[visibility_level]** = `0/Everyone`
  * **group[members_visibility_level]** = `0/Everyone`
* **private_roster** is `1/members` and **subscribe_policy** is `0/open` or `1/confirm`:
  * **group[public_admission]** = 'true'
  * **group[allow_membership_requests]** = 'false'
  * **group[visibility_level]** = `0/Everyone`
  * **group[members_visibility_level]** = `2/Members`
* **private_roster** is `2/admins` and **subscribe_policy** is `0/open` or `1/confirm`:
  * **group[public_admission]** = 'true'
  * **group[allow_membership_requests]** = 'false'
  * **group[visibility_level]** = `2/Group owners and members`
  * **group[members_visibility_level]** = `3/Group owners and staff`
* **private_roster** is `0/public` and **subscribe_policy** is `2/moderate` or `3/confirm_then_moderate`:
  * **group[public_admission]** = 'false'
  * **group[allow_membership_requests]** = 'true'
  * **group[visibility_level]** = `0/Everyone`
  * **group[members_visibility_level]** = `0/Everyone`
* **private_roster** is `1/members` and **subscribe_policy** is `2/moderate` or `3/confirm_then_moderate`:
  * **group[public_admission]** = 'false'
  * **group[allow_membership_requests]** = 'true'
  * **group[visibility_level]** = `0/Everyone`
  * **group[members_visibility_level]** = `2/Members`
* **private_roster** is `2/admins` and **subscribe_policy** is `2/moderate` or `3/confirm_then_moderate`:
  * **group[public_admission]** = 'false'
  * **group[allow_membership_requests]** = 'false' it means the **subscribe_policy** is modified, because it is not possible to allow membership requetss for a group that is not publicly visible
  * **group[visibility_level]** = `2/Group owners and members`
  * **group[members_visibility_level]** = `3/Group owners and staff`

Access control and moderation
-----------------------------

The `config.pck` fields **default_member_moderation** and
**member_moderation_action** describe the moderation policy and are
mapped as follows:

* **default_member_moderation** exist.
  * **member_moderation_action** is `0/Hold`: **moderation** = `approval`.
  * **member_moderation_action** is `1/Reject`: **moderation** = `ignore`.
    Reject implies a reply is sent back to the sender to notify them the message
    has been rejected. However discourse does not have this functionality and can
    only ignore a message that should have been rejected.
  * **member_moderation_action** is `2/Discard`: **moderation** = `ignore`.
* **default_member_moderation** does not exist: **moderation** = `no`.

The `config.pck` fields **archive** and **archive_private** determine
if the archives are visible to the public or limited to the mailing
list members. They are mapped as follows:

* **archive** is set.
  * **archive_private** is set: **archive** = `private`.
  * **archive_private** is not set: **archive** = `public`.
* **archive** is not set: **archive** = `private`.
  If **archive** is not set, the mailing list does not keep any archive. However
  it is not possible to configure discourse to not keep a copy of the messages
  and the closest fallback is to keep them private.

The `config.pck` fields that define how members join the list, post
message and view the archives are mapped to the following category settings:

* **email_in_allow_strangers**: if `true`, accept emails from anonymous users with no accounts.
* **group_permissions[thelist-members]**: if set to `1`, members of the `thelist-members` group can Create/Reply/See
  messages in the category.
* **group_permissions[everyone]**: if set to `1`, everyone can `Create/Reply/See` messages in
  the category, if set to `3` everyone can `See` messages . It superseeds **group_permissions[thelist-members]**.
* **custom_fields[require_topic_approval]** and **custom_fields[require_reply_approval]**: if `true`,
  require approval from a member of the `thelist-moderators` group for all new topics and replies.

The mapping is done as follows (when the field is not set, it is not mentionned):

* **moderation** is `no` and **archive** is `public`.
  * **email_in_allow_strangers** = `true`
  * **group_permissions[everyone]** = `1/Create/Reply/See`
* **moderation** is `no` and **archive** is `private`.
  * **email_in_allow_strangers** = `true`
  * **group_permissions[thelist-members]** = `1/Create/Reply/See`
* **moderation** is `ignore` and **archive** is `public`.
  * **email_in_allow_strangers** = `false`
  * **group_permissions[thelist-members]** = `1/Create/Reply/See`
  * **group_permissions[everyone]** = `3/See`.
  A registered user that is not a member is not ignored, they will get an error message.
  Incoming emails from unregistered users will be ignored.
* **moderation** is `ignore` and **archive** is `private`.
  * **email_in_allow_strangers** = `false`
  * **group_permissions[thelist-members]** = `1/Create/Reply/See`
  A registered user that is not a member is not ignored, they will get an error message.
  Incoming emails from unregistered users will be ignored.
* **moderation** is `approval` and **archive** is `public`.
  * **email_in_allow_strangers** = `true`
  * **group_permissions[thelist-members]** = `1/Create/Reply/See`
  * **group_permissions[everyone]** = `3/See`.
  * **custom_fields[require_topic_approval]** = `true`
  * **custom_fields[require_reply_approval]** = `true`
* **moderation** is `approval` and **archive** is `private`.
  * **email_in_allow_strangers** = `true`
  * **group_permissions[thelist-members]** = `1/Create/Reply/See`
  * **custom_fields[require_topic_approval]** = `true`
  * **custom_fields[require_reply_approval]** = `true`

Note that the **moderation** field does not exist in `config.pck`, it
is derived from **default_member_moderation** as explained above.

Note that the **archive** field value is derived from **archive** and
**archive_private** as explained above.

Discarded
---------

* **preferred_language**: it is not possible to set the interface
  language on a per-category basis
* **digest_members**: it is not possible to request a digest mode
  on a per-category basis.

Development
===========

* virtualenv --python=python3 venv
* source venv/bin/activate
* pip install pipenv
* pipenv install --dev
* pipenv run pipenv_to_requirements -f
* tests/build-discourse
* echo $(cat v2.5.5/ip) forumv2.5.5.example.com | sudo tee -a /etc/hosts
* firefox http://forumv2.5.5.example.com # user: api, password: BefShnygs33SwowCifViwag
* tox
* PYTEST_ADDOPTS="--color=no" ../mailman2discourse-virtualenv/bin/tox -e py3 -- --discourse v2.6.0 -k test_category_set tests/test_discourse.py
* When discourses fails with "Internal Server Error", details about the error can be found in http://forumv2.6.0.example.com/logs/
* When the sidekiq queue grows too much http://forumv2.5.5.example.com/sidekiq shows which jobs are waiting
* In about:config disable security.csp.enable while testing otherwise it will prevent loading from non-https

Release support
===============

Tests are run on a set of supported discourse releases. When adding a new
release (for instance v2.6.0, the following files must be updated)

* tox.ini update --discourse argument
* .gitlab-ci.yml update container deletion
* tests/build-discourse figure out which commit hash of discourse_docker matches
  a given version and add it using v2.5.5 as a model

Release management
==================

* Prepare a new version

 - version=1.3.0 ; rm -f inventory/hosts.yml ; perl -pi -e "s/^version.*/version = $version/" setup.cfg ; for i in 1 2 ; do python setup.py sdist ; amend=$(git log -1 --oneline | grep --quiet "version $version" && echo --amend) ; git commit $amend -m "version $version" ChangeLog setup.cfg ; git tag -a -f -m "version $version" $version ; done
 - git push ; git push --tags
 - twine upload -s --username enough --password "$ENOUGH_PYPI_PASSWORD" dist/mailman2discourse-$version.tar.gz
