# Fluxo Git Flow: Feature → Develop → Release → Main

## 1. Atualizar a branch `develop`

Antes de iniciar uma nova funcionalidade, atualize sua cópia local da `develop`.

```bash
git checkout develop
git pull origin develop
```

---

## 2. Criar uma branch de `feature`

Crie a branch de funcionalidade a partir da `develop`.

```bash
git checkout -b feature/nome-da-feature
```

Exemplo:

```bash
git checkout -b feature/cadastro-alunos
```

---

## 3. Desenvolver e realizar os commits

Faça as alterações necessárias e registre os commits:

```bash
git add .
git commit -m "feat: implementa cadastro de alunos"
```

---

## 4. Publicar a branch `feature`

Envie a branch para o GitHub:

```bash
git push -u origin feature/nome-da-feature
```

Exemplo:

```bash
git push -u origin feature/cadastro-alunos
```

Depois, abra um **Pull Request** no GitHub:

```text
feature/cadastro-alunos → develop
```

Após a aprovação, faça o merge do Pull Request na `develop`.

---

## 5. Excluir a branch `feature`

Depois que a `feature` for mesclada na `develop`, exclua a branch local:

```bash
git branch -d feature/nome-da-feature
```

Exemplo:

```bash
git branch -d feature/cadastro-alunos
```

Exclua também a branch remota:

```bash
git push origin --delete feature/nome-da-feature
```

---

# Release

## 6. Atualizar a branch `develop`

Antes de criar uma release, certifique-se de que a `develop` está atualizada:

```bash
git checkout develop
git pull origin develop
```

---

## 7. Criar a branch de `release`

Crie a branch de release a partir da `develop`:

```bash
git checkout -b release/1.0.0
```

Exemplo:

```bash
git checkout -b release/1.0.0
```

A partir deste momento, a branch `release` deve receber apenas ajustes finais da versão, como correções, documentação e preparação da versão.

---

## 8. Publicar a branch `release`

Envie a branch para o GitHub:

```bash
git push -u origin release/1.0.0
```

---

## 9. Criar a `tag`

Quando a release estiver pronta, crie uma tag de versão:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
```

Confira a tag:

```bash
git tag
```

---

## 10. Publicar a `tag`

Envie a tag para o GitHub:

```bash
git push origin v1.0.0
```

Ou, para publicar todas as tags:

```bash
git push origin --tags
```

---

## 11. Publicar a Release no GitHub

No GitHub:

1. Acesse **Releases**.
2. Clique em **Draft a new release**.
3. Selecione a tag `v1.0.0`.
4. Informe o título da release.
5. Adicione as notas da versão.
6. Clique em **Publish release**.

---

# Mesclando a Release

## 12. Mesclar `release` na `main`

Atualize a `main`:

```bash
git checkout main
git pull origin main
```

Faça o merge da release:

```bash
git merge --no-ff release/1.0.0
```

Envie a `main` para o GitHub:

```bash
git push origin main
```

---

## 13. Mesclar `release` na `develop`

Depois de atualizar a `main`, volte para a `develop`:

```bash
git checkout develop
git pull origin develop
```

Faça o merge da release:

```bash
git merge --no-ff release/1.0.0
```

Envie a `develop` para o GitHub:

```bash
git push origin develop
```

---

## 14. Excluir a branch `release`

Depois que a release tiver sido mesclada tanto na `main` quanto na `develop`, exclua a branch local:

```bash
git branch -d release/1.0.0
```

Exclua também a branch remota:

```bash
git push origin --delete release/1.0.0
```

---

# Fluxo resumido

```text
                    ┌──────────────┐
                    │    develop   │
                    └──────┬───────┘
                           │
                           │ criar
                           ▼
                    ┌──────────────┐
                    │    feature   │
                    └──────┬───────┘
                           │
                           │ Pull Request
                           ▼
                    ┌──────────────┐
                    │    develop   │
                    └──────┬───────┘
                           │
                           │ criar release
                           ▼
                    ┌──────────────┐
                    │    release   │
                    └──────┬───────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
             ┌────────┐        ┌──────────┐
             │  main  │        │ develop  │
             └────────┘        └──────────┘
                 │
                 ▼
              v1.0.0
                TAG
```

## Sequência completa de comandos

```bash
# DEVELOP
git checkout develop
git pull origin develop

# FEATURE
git checkout -b feature/nome-da-feature
git add .
git commit -m "feat: descrição da alteração"
git push -u origin feature/nome-da-feature

# Após o Pull Request: feature → develop

git checkout develop
git pull origin develop
git branch -d feature/nome-da-feature
git push origin --delete feature/nome-da-feature

# RELEASE
git checkout develop
git pull origin develop
git checkout -b release/1.0.0
git push -u origin release/1.0.0

# TAG
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# MAIN
git checkout main
git pull origin main
git merge --no-ff release/1.0.0
git push origin main

# DEVELOP
git checkout develop
git pull origin develop
git merge --no-ff release/1.0.0
git push origin develop

# EXCLUIR RELEASE
git branch -d release/1.0.0
git push origin --delete release/1.0.0
```

**Fluxo final:**

```text
feature → develop → release → main
                         └──→ develop
```

A `tag` (`v1.0.0`) deve ficar associada ao commit da versão publicada e **não deve ser excluída junto com a branch `release`**.
