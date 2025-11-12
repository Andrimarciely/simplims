from faker import Faker


fake = Faker("pt_BR")
FAKE_CNPJ, FAKE_CPF = fake.company_id(), fake.ssn()
