![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)
![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)


# Snapsheets

Wget snapshots of Google 

---

# Usage

```python
>>> import snapsheets as ss
>>> ss.add_config('test_config.yml')
>>> ss.get('test1', by='wget')
```

---

## Config

- Write config file in ``YAML`` format

```yaml
volumes:
  snapd: 'data/'

options:
  wget:
    '--quiet'
    
sheets:
  test1:
    key: '1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM'
    gid: 'None'
    format: 'xlsx'
    sheet_name:
      - 'シート1'
      - 'シート2'
    stem: 'test_sheet'
    datefmt: '%Y'
```

---

# Documents

- https://shotakaha.gitlab.io/snapsheets/
