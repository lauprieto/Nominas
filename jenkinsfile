pipeline {
    agent any

    stages {
        stage('Instalar dependencias') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '. venv/bin/activate && pytest --tb=short --disable-warnings'
            }
        }
    }

    post {
        always {
            junit '**/test-results.xml'
        }
    }
}
