#!/bin/bash

echo "====================================="
echo "        COMMIT AUTOMÁTICO GIT"
echo "====================================="
echo

read -p "Mensagem do commit: " mensagem

if [ -z "$mensagem" ]; then
    echo
    echo "❌ Commit cancelado. Nenhuma mensagem informada."
    exit 1
fi

echo
echo "📦 Adicionando arquivos..."
git add .

echo
echo "📝 Criando commit..."
git commit -m "$mensagem"

if [ $? -ne 0 ]; then
    echo
    echo "❌ Não foi possível criar o commit."
    exit 1
fi

echo
echo "🚀 Enviando para a branch main..."
git push origin main

echo
echo "✅ Commit enviado com sucesso!"
