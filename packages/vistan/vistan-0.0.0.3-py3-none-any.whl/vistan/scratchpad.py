import os
import shutil
import traceback
from utilities import open_pickled_files    


def transfer_model_files_from_orig_to_model():
    # + Go through the models
    # + for each model
    #   + load the code, and the data
    #   + save the code and the data

    source_dir = "./eg_stan/"
    target_dir = "./models"
        
    file_names = os.listdir(source_dir)
        

    # shutil.move(source, dest)  

    good_model_paths = (open_pickled_files("../data/utilities/good_model_paths.pkl"))
    good_model_orig_id_dict = (open_pickled_files("../data/utilities/good_model_new_id_to_old_id_dict.pkl"))

    for m in range(1, 31):

        model_path = good_model_paths[good_model_orig_id_dict[m]]
        root, model_name = model_path
        source_dir = "./"+root
        file_names = os.listdir(source_dir)
        for file_name in file_names:

            try:

                shutil.move(os.path.join(source_dir, file_name), target_dir)

            except Exception:

                 print(traceback.print_exc())

def change_the_name_dict():
    good_model_names = (open_pickled_files("../data/utilities/good_model_name.pkl"))
    good_model_orig_id_dict = (open_pickled_files("../data/utilities/good_model_new_id_to_old_id_dict.pkl"))

    print(good_model_orig_id_dict)
def test_vistan():
    model = """
        data {
            int<lower=0> N; 
            int<lower=0,upper=1> switc[N];
        }
        parameters {
             real<lower=0,upper=1> beta1;
             real<lower=2,upper=2.4> beta2;
        } 
        model {
            switc ~ bernoulli(beta1);
        }
    """

    data = {"N" : 2, "switc": [1,0]}



# change_the_name_dict()
def test_pystan():
    import pystan
    import pickle
    import warnings
    from mystan import suppress_stdout_stderr, is_good_model
    from collections import OrderedDict
    model = """
        data {
            int<lower=0> N; 
            int<lower=0,upper=1> switc[N];
        }
        parameters {
             real<lower=0,upper=1> beta1;
             real<lower=2,upper=2.4> beta2;
        } 
        model {
            switc ~ bernoulli(beta1);
        }
    """

    data = {"N" : 2, "switc": [1,0]}

    print(is_good_model(model, data, model_name = "test_model"))
    exit()
    # def get_lop(model, data):

    try:
        with open("./test-model.pkl", "rb") as f:
            m = pickle.load(f)
    except:
        print("Did not find cached model. Re-compiling...")
        try: 
            with suppress_stdout_stderr(verbose = False):
                m = pystan.StanModel(model_code = model)
        except:
            print("Errors during recompile...")
            raise 
        print("Finished recompiling...")
        with open("./test-model.pkl", "wb") as f:
            pickle.dump(m, f)
        print("Model recompiled and cached...")

    with suppress_stdout_stderr(verbose = False):
        fit4 = m.sampling(data = data, chains = 1, iter = 10, seed = 0)
    # try : 
    #     with suppress_stdout_stderr(True):
    #         # print("blah blah")
    #         a = 1/0
    # except :
    #     pass
    # raise 
    # print("somehtign")
    # print (traceback.print_exc())
    # exit()

    print(fit4.extract()["beta1"].shape)   
    print(fit4.extract())   

    # exit()
    keys = fit4.unconstrained_param_names()
    z_len = len(keys)
    # print(z_len)
    # exit()
    """
    
    We want to constrain these parameters and then provide them in the shape of a dictionary
    
    """
    def constrain_params(z):

        assert z.shape[-1] == z_len

        return np.array([fit4.constrain_pars(np.asarray(z_, order = "C")) for z_ in z])

    def get_n_samples(z):

        assert z.ndim == 2
        return z.shape[0]

    def array_to_dict(z):

        assert z.shape[-1] == z_len
        assert get_n_samples(z) >= 1 

        dz = OrderedDict()

        for i,k in enumerate(keys):
            dz[k] = z[:,i] 

        return dz

    def unconstrain_params(z):

        N = get_n_samples(z)
        dz = array_to_dict(z)

        return np.array([fit4.unconstrain_pars({k:v[n] for k,v in dz.items()}) \
                                for n in range(N)])


    N = 5

    z = np.random.randn(N*2).reshape(N,2).astype(float)

    z_cons = (constrain_params(z))
    print(array_to_dict(z_cons))

    z_uncons = unconstrain_params(z_cons)
    print(array_to_dict(z_uncons))

    print(z)
    with suppress_stdout_stderr(verbose = False):
        rez = m.vb(data=data,algorithm="meanfield", output_samples = 10, sample_file = "./samples")
    z_vb = np.array(rez['sampler_params']).T[:,:-1]
    print(f"Unconstrained VB samples {z_vb}")
    print(f"Constrained VB samples {constrain_params(z_vb)}")
    print(f"Constrained VB samples {array_to_dict(z_vb)}")
    print(f"log p at z_cons: {fit4.log_prob(z_vb[0, :], adjust_transform = False)}")
    # print(f"grad log p at z_cons: {fit4.grad_log_prob(z_vb[0, :], adjust_transform = False)}")
    # print(f"grad log p at z_cons: {fit4.grad_log_prob(z_vb[0, :], adjust_transform = True)}")
    print(f"log p at z_uncons {fit4.log_prob(unconstrain_params(z_vb)[0,:], adjust_transform = True)}")
    print(f"log p at z_uncons {fit4.log_prob((z_vb)[0,:], adjust_transform = True)}")
# test_pystan()
# def test_dicts():
#     from collections import OrderedDict
#     a = {"s": "S", "t" : "T"}
#     b = OrderedDict(**a)
#     print(a)
#     print(a)
#     print(a)
#     print(a)
#     print(a)
#     print("ordered")
#     print(b)
#     print(b)
#     print(b)
#     print(b)
#     print(b)
# test_dicts()
def test_imports():
    import inference
    import interface

test_imports()

"""
We need to take care of verbose.
We need to clean the UI to take only model and data as inputs.
We need to put this all in a nice pip package.
"""